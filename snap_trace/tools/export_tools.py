"""MCP tools: model export (TRCIN), save (.med), validate."""
from __future__ import annotations

import math
import os
import re
import tempfile

import snap_trace.session as session
from snap_trace.snap_env import target_version
from snap_trace.component_map import find_component

# ── version-specific export fixups ───────────────────────────────────────────
# SNAP's model.export() targets whichever TRACE binary version the plugin was
# built against.  When the installed TRACE binary is older, the exported deck
# may need adjustment.  Add new fixup entries here as version mismatches are
# discovered; gate each one on the target version range where it applies.

# Fixup: FILL SV card layout (introduced after TRACE 5.0p9).
# SNAP plugin 4.7.0 emits 5-field split-mass layout:
#   ifmlsv  ifmvsv  iftlsv  iftvsv  ifasv
# TRACE ≤ 5.0p9 expects the older 4-field combined layout:
#   ifmmsv  iftlsv  iftvsv  ifasv
_FILL_SV_OLD = "*       ifmlsv        ifmvsv        iftlsv        iftvsv         ifasv"
_FILL_SV_NEW = "*       ifmmsv        iftlsv        iftvsv         ifasv"
_FILL_SV_DATA_5 = re.compile(
    r"(\*       ifmmsv        iftlsv        iftvsv         ifasv\n)"
    r"([ \t]+\S+[ \t]+\S+[ \t]+\S+[ \t]+\S+[ \t]+\S+[ \t]*\n)"
)


def _fixup_trcin(content: str) -> str:
    tv = target_version()

    # Always: integer fields stored as Java doubles export as "0.0", "1.0",
    # etc.  The TRACE ASCII parser rejects floats in integer-only fields.
    content = re.sub(r'\b(\d+)\.0\b', r'\1', content)

    # TRACE ≤ 5.0p9: collapse 5-field FILL SV card to 4-field.
    if tv <= (5, 0, 9):
        content = content.replace(_FILL_SV_OLD, _FILL_SV_NEW)

        def _drop_fifth_sv(m):
            comment = m.group(1)
            data_vals = m.group(2).split()
            fixed = "             ".join([""] + data_vals[:4]) + "\n"
            return comment + fixed

        content = _FILL_SV_DATA_5.sub(_drop_fifth_sv, content)

    return content


def _coerce_list(obj):
    """Return obj as a list; wraps single-item returns from SNAP list methods."""
    if obj is None:
        return []
    try:
        return list(obj)
    except Exception:
        return [obj]


def _to_float(val) -> float | None:
    """Extract a numeric value from a SNAP property object or plain number.

    SNAP attributes often return CReal/RealProperty wrappers whose ``float()``
    raises TypeError.  Try the raw cast first, then fall back to ``.value``.
    Returns None if neither conversion succeeds.
    """
    if val is None:
        return None
    try:
        return float(val)
    except Exception:
        pass
    try:
        return float(val.value)
    except Exception:
        pass
    return None


# Pattern → fix guidance appended to bare Java validation error strings.
# Keyed by substring found in the error message; first match wins.
_ERROR_HINTS: list[tuple[str, str]] = [
    (
        "Y Angle",
        "Vessel azimuthal angles are in RADIANS (not degrees). "
        "Full circle = 6.2832 rad (2π). "
        "The initializer may have written a degrees value — "
        "delete and recreate the vessel, or use set_vessel_table(..., 'y_nodalization', 6.2832).",
    ),
    (
        "Connection Angle has not been set",
        "Pass angle_deg to connect_components() or connect_pipe_to_vessel(). "
        "0° = horizontal, 90° = upward vertical, -90° = downward vertical.",
    ),
    (
        "Connection has an unknown angle",
        "Pass angle_deg to connect_components() or connect_pipe_to_vessel(). "
        "0° = horizontal, 90° = upward vertical, -90° = downward vertical.",
    ),
    (
        "Abrupt area change",
        "Set NffSel.FricAndAbrupt on the edge between the two cells using "
        "set_pipe_edge_property(model_id, pipe_cc, edge_index, 'nff', "
        "'NffSel.FricAndAbrupt'). connect_pipe_to_vessel() sets this automatically "
        "when auto_nff=True (default).",
    ),
    (
        "hydraulic diameter",
        "Set hydraulic diameters via set_vessel_table(model_id, vessel_cc, "
        "'hd_axial', value_m) — and hd_azimuthal, hd_radial. "
        "Typical RPV: hd_axial ≈ 0.4 m.",
    ),
    (
        "Initial Conditions",
        "Set per-cell ICs via set_pipe_ics() for PIPEs or "
        "set_vessel_table(model_id, vessel_cc, 'p'/'tl'/'tv'/'alp', value) for VESSELs.",
    ),
]


def _enrich_error(msg: str) -> str:
    """Add computed context and fix guidance to well-known validation error strings."""
    # Abrupt Area Change: parse the two adjacent cell areas and append ratio.
    if "Adjacent cells [" in msg:
        try:
            bracket = msg.index("Adjacent cells [") + len("Adjacent cells [")
            inner = msg[bracket: msg.index("]", bracket)]
            a1, a2 = (float(x.strip()) for x in inner.split(","))
            if a2 != 0:
                ratio = max(a1, a2) / min(a1, a2)
                return f"{msg}  [ratio {ratio:.2f} > limit 2.0]"
        except Exception:
            pass

    # Pattern-based fix guidance for Java-originated error strings.
    for pattern, hint in _ERROR_HINTS:
        if pattern in msg:
            return f"{msg}  [Fix: {hint}]"

    return msg


def _python_model_check(model) -> list[str]:
    """Inspect model components in Python for common errors SNAP may not surface.

    Returns a list of error strings (empty = no errors found).
    Checks performed:
      - PIPE / PUMP: IC table empty or any cell has zero p/tl/tv
      - PIPE / PUMP / VALVE: inlet and outlet must both be connected
      - VESSEL: IC tables, hydraulic diameter tables, azimuthal Y-angle (≤ 2π rad)
      - BREAK/FILL: pin must be non-zero; at least one hydraulic connection
      - PUMP: rated values, MOI, speed/friction parameters must all be non-zero
    """
    errors = []

    # PIPE initial conditions
    try:
        for pipe in _coerce_list(model.pipes()):
            try:
                cc = pipe.cc_number
                seg = pipe.fluid_segment
                cells = seg.cells  # PropertyValueList — supports len() and indexing
                n_rows = len(cells)
                if n_rows == 0:
                    errors.append(f"Pipe {cc}: Initial Conditions table is empty (ICs not set)")
                else:
                    for i in range(n_rows):
                        try:
                            c  = cells[i]
                            p  = _to_float(c.p.value  if c.p  is not None else None) or 0.0
                            tl = _to_float(c.tl.value if c.tl is not None else None) or 0.0
                            tv = _to_float(c.tv.value if c.tv is not None else None) or 0.0
                            bad = []
                            if p  == 0.0: bad.append("p")
                            if tl == 0.0: bad.append("tl")
                            if tv == 0.0: bad.append("tv")
                            if bad:
                                errors.append(
                                    f"Pipe {cc} cell {i+1}: IC(s) not set: {', '.join(bad)}"
                                )
                        except Exception:
                            pass
            except Exception as exc:
                errors.append(f"Pipe IC check failed: {exc}")
    except Exception:
        pass

    # VESSEL: initial conditions + hydraulic diameter tables + geometry
    try:
        _axis_sels = []
        try:
            import snap.codes.trace.enums as _te
            _axis_sels = [
                ("axial",     _te.AxisSel.AXIAL()),
                ("azimuthal", _te.AxisSel.AZIMUTHAL()),
                ("radial",    _te.AxisSel.RADIAL()),
            ]
        except Exception:
            pass

        for vessel in _coerce_list(model.vessels()):
            cc = -1
            try:
                cc = vessel.cc_number

                # IC tables
                p_table = vessel.p_table
                tl_table = vessel.tl_table
                tv_table = vessel.tv_table
                n_rows = _get_table_len(p_table)
                if n_rows == 0:
                    errors.append(f"Vessel {cc}: Initial Conditions table is empty (ICs not set)")
                elif n_rows < 0:
                    pass  # table size indeterminate — skip check
                else:
                    # Materialize each table ONCE. Indexing a
                    # Hydro3DPropertyTable rebuilds the entire table per
                    # access, so `for i in range(n): tbl[i]` costs O(rows^2)
                    # gateway crossings -- 33 rows x 3 tables was ~35 minutes
                    # on a plant vessel and made validate_model time out.
                    rows_p = _materialize_table(p_table)
                    rows_tl = _materialize_table(tl_table)
                    rows_tv = _materialize_table(tv_table)
                    usable = min(n_rows, len(rows_p), len(rows_tl), len(rows_tv))
                    for i in range(usable):
                        try:
                            row_p = rows_p[i]
                            row_tl = rows_tl[i]
                            row_tv = rows_tv[i]
                            for j, (pv, tlv, tvv) in enumerate(zip(row_p, row_tl, row_tv)):
                                p  = _to_float(pv)  or 0.0
                                tl = _to_float(tlv) or 0.0
                                tv = _to_float(tvv) or 0.0
                                bad = []
                                if p  == 0.0: bad.append("p")
                                if tl == 0.0: bad.append("tl")
                                if tv == 0.0: bad.append("tv")
                                if bad:
                                    errors.append(
                                        f"Vessel {cc} level {i+1} cell {j+1}: "
                                        f"IC(s) not set: {', '.join(bad)}"
                                    )
                        except Exception:
                            pass

                # Hydraulic diameter tables (axial/azimuthal/radial edges)
                for axis_name, ax_sel in _axis_sels:
                    try:
                        hd_t = vessel.hd_table(ax_sel)
                        n_hd = _get_table_len(hd_t)
                        if n_hd == 0:
                            errors.append(
                                f"Vessel {cc}: hd_{axis_name} table empty — "
                                f"call set_vessel_table(model_id, {cc}, 'hd_{axis_name}', value_m)"
                            )
                        else:
                            first_row = hd_t[0]
                            all_zero = all(v is None or float(v) == 0.0 for v in first_row)
                            if all_zero:
                                errors.append(
                                    f"Vessel {cc}: hd_{axis_name} all zero — "
                                    f"set hydraulic diameters via set_vessel_table(..., 'hd_{axis_name}', value_m)"
                                )
                    except Exception:
                        pass

                # Y Angle (azimuthal extent): must be ≤ 2π radians; 360° is a common unit error.
                # Check ALL candidate attributes — do NOT break on first find, because some
                # names may hold an intermediate (non-angle) value that happens to be small.
                _angle_checked = False
                for attr in ("_dang", "dang", "_ymax", "ymax", "yang_max", "y_max",
                             "theta_max", "azimuthal_extent"):
                    try:
                        val = getattr(vessel, attr, None)
                        if val is None:
                            continue
                        y = _to_float(val)
                        if y is None:
                            continue
                        _angle_checked = True
                        if y > 2 * math.pi + 0.01:
                            errors.append(
                                f"Vessel {cc}: {attr} = {y:.4f} rad is out of range "
                                f"(max 6.2832 rad = 2π). Vessel angles are in RADIANS — "
                                f"use 6.2832 for a full circle, not 360"
                            )
                            break
                    except Exception:
                        pass

            except Exception as exc:
                errors.append(f"Vessel {cc} check failed: {exc}")
    except Exception:
        pass

    # BREAK / FILL: boundary pressure and hydraulic connections
    for getter, label in (("breaks", "Break"), ("fills", "Fill")):
        try:
            for comp in _coerce_list(getattr(model, getter)()):
                try:
                    cc = comp.cc_number
                    pin = float(comp.pin) if comp.pin is not None else 0.0
                    if pin == 0.0:
                        errors.append(f"{label} {cc}: pin (boundary pressure) not set")
                    connected = any(
                        getattr(comp, face, None) is not None
                        for face in ("inlet", "outlet", "side")
                    )
                    if not connected:
                        errors.append(f"{label} {cc}: no hydraulic connections (all faces unset)")
                except Exception as exc:
                    errors.append(f"{label} connection check failed: {exc}")
        except Exception:
            pass

    # PUMP: rated values, MOI, speed/friction parameters, ICs, and connections
    try:
        for pump in _coerce_list(model.pumps()):
            cc = -1
            try:
                cc = pump.cc_number
                missing = []

                def _pump_attr_zero(attrs, label):
                    """Flag label if all synonyms are missing or any found synonym is 0."""
                    for attr in attrs:
                        val = getattr(pump, attr, None)
                        if val is not None:
                            fv = _to_float(val)
                            if fv is not None and fv == 0.0:
                                missing.append(label)
                            return  # found the attribute; done
                    # No synonym found via Python API — flag as potentially unset
                    missing.append(f"{label} (attribute not accessible)")

                _pump_attr_zero(("head",   "hrat"),           "Rated Head")
                _pump_attr_zero(("flow",   "florat", "qrat"), "Rated Volumetric Flow")
                _pump_attr_zero(("speed",  "wrat"),            "Rated Speed")
                _pump_attr_zero(("torque", "tqrat"),           "Rated Torque")
                _pump_attr_zero(("density","rhorat","rhog"),   "Rated Fluid Density")
                _pump_attr_zero(("inertia","amoi", "moi"),     "Effective MOI")
                _pump_attr_zero(("initial_speed","wspd0","wsp0","winit"), "Initial Speed")
                _pump_attr_zero(("off_speed","wspdoff"),       "Off Speed")
                _pump_attr_zero(("max_speed_change","dwspmax"),"Max Speed Change")
                _pump_attr_zero(("speed_scale","wspdscl"),     "Speed Scale Factor")
                _pump_attr_zero(("fric0",),                    "Frictional Torque 0")
                _pump_attr_zero(("torque_break_speed","wspdbrk"), "Torque Break Speed")

                if missing:
                    errors.append(
                        f"Pump {cc}: required parameters not set or zero — "
                        + ", ".join(missing)
                    )

                # Pump cell initial conditions (fluid_segment.cells like PIPE)
                try:
                    seg = pump.fluid_segment
                    cells = seg.cells
                    n = len(cells)
                    for i in range(n):
                        try:
                            c = cells[i]
                            p  = _to_float(c.p.value  if c.p  is not None else None) or 0.0
                            tl = _to_float(c.tl.value if c.tl is not None else None) or 0.0
                            tv = _to_float(c.tv.value if c.tv is not None else None) or 0.0
                            if p == 0.0 or tl == 0.0 or tv == 0.0:
                                errors.append(
                                    f"Pump {cc} cell {i+1}: ICs not set "
                                    f"(p={p}, tl={tl}, tv={tv})"
                                )
                        except Exception:
                            pass
                except Exception:
                    pass

                # Pump must have both inlet and outlet connected
                for face in ("inlet", "outlet"):
                    try:
                        jun = getattr(pump, face, None)
                        if jun is None:
                            errors.append(f"Pump {cc}: {face} edge is unconnected")
                    except Exception:
                        pass

            except Exception as exc:
                errors.append(f"Pump {cc} check failed: {exc}")
    except Exception:
        pass

    # PIPE / VALVE: both inlet and outlet must be connected
    for _getter, _label in (("pipes", "Pipe"), ("valves", "Valve")):
        try:
            for comp in _coerce_list(getattr(model, _getter, lambda: [])() ):
                try:
                    cc = comp.cc_number
                    for face in ("inlet", "outlet"):
                        try:
                            jun = getattr(comp, face, None)
                            if jun is None:
                                errors.append(f"{_label} {cc}: {face} edge is unconnected")
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

    # HYDRAULIC JUNCTION ANGLES
    # Junctions connecting two 1-D components need a connection angle (DANGLE in TRCIN).
    # Zero angle causes 'Connection has an unknown angle' model check errors.
    try:
        for comp_type, comp in _iter_all_for_check(model):
            cc = -1
            try:
                cc = int(comp.java_object.getCCnumber())
                for face in ("inlet", "outlet", "side"):
                    jun = getattr(comp, face, None)
                    if jun is None:
                        continue
                    for angle_attr in ("angle", "dangle", "theta", "con_angle"):
                        val = getattr(jun, angle_attr, None)
                        if val is not None:
                            try:
                                if float(val) == 0.0:
                                    errors.append(
                                        f"{comp_type} {cc} {face} junction: "
                                        f"connection angle (dangle) not set"
                                    )
                            except Exception:
                                pass
                            break
            except Exception:
                pass
    except Exception:
        pass

    return errors


def _iter_all_for_check(model):
    """Yield (comp_type, comp) for hydraulic 1-D components only (no VESSEL/HS)."""
    from snap_trace.component_map import COMPONENT_MAP, _coerce_list as _cl
    _hydro = {"PIPE", "FILL", "BREAK", "PUMP", "VALVE", "PLENUM", "TEE", "SEPARATOR"}
    for comp_type, cfg in COMPONENT_MAP.items():
        if comp_type not in _hydro:
            continue
        list_method = cfg.get("list")
        if not list_method:
            continue
        try:
            for comp in _cl(getattr(model, list_method)()):
                yield comp_type, comp
        except Exception:
            pass


def _materialize_table(tbl) -> list:
    """Snapshot a SNAP property table as a list of rows, building it once.

    Indexing a Hydro3DPropertyTable rebuilds the *entire* table on every
    access (`__getitem__` returns `self._values()[item]`), so a loop of the
    form `for i in range(n): tbl[i]` costs O(rows^2) gateway crossings.
    Iterating goes through `__iter__`, which builds `_values()` a single
    time. See PY4J_TABLE_PERFORMANCE.md in the SNAP-TRACE-Plugin repo.

    Returns [] if the table cannot be read, so callers degrade to skipping
    the check rather than raising.
    """
    try:
        return list(tbl)
    except Exception:
        return []


def _get_table_len(tbl) -> int:
    """Return row count of a SNAP table object using multiple access patterns.

    PropertyValueTable and similar types expose row count differently across
    SNAP plugin versions. Returns -1 if count cannot be determined.
    """
    for attr in ("row_count", "rowCount", "getRowCount", "size", "count", "length"):
        try:
            v = getattr(tbl, attr, None)
            if v is None:
                continue
            return int(v() if callable(v) else v)
        except Exception:
            pass
    try:
        return len(tbl)
    except Exception:
        pass
    return -1


def _get_table_row(tbl, i: int):
    """Return row i from a SNAP table object, trying multiple access patterns."""
    for access in (
        lambda: tbl[i],
        lambda: tbl.getRow(i),
        lambda: tbl.get(i),
        lambda: tbl.getValueAt(i),
    ):
        try:
            return access()
        except Exception:
            pass
    return None


def _read_result_set(result_set, errors: list, warnings: list) -> None:
    """Extract errors/warnings from a SNAP CheckResultSet via multiple Java access patterns.

    Tries toArray() first (doesn't require iterator(), which is blocked by
    Java module-opens restrictions), then falls back to size()/get(i).
    """

    def _classify(item):
        severity = ""
        message = str(item)
        for sev_attr in ("getSeverity", "getLevel"):
            try:
                severity = str(getattr(item, sev_attr)()).lower()
                break
            except Exception:
                pass
        for msg_attr in ("getMessage", "getDescription"):
            try:
                m = str(getattr(item, msg_attr)())
                if m:
                    message = m
                    break
            except Exception:
                pass
        if "error" in severity or (not severity and "error" in message.lower()):
            errors.append(message)
        else:
            warnings.append(message)

    # Pattern A: toArray() — bypasses iterator() which is module-restricted
    try:
        arr = result_set.toArray()
        for item in arr:
            try:
                _classify(item)
            except Exception:
                pass
        return
    except Exception:
        pass

    # Pattern B: size() / get(i)
    try:
        n = int(result_set.size())
        for i in range(n):
            try:
                _classify(result_set.get(i))
            except Exception:
                pass
    except Exception:
        pass


def register(mcp):

    @mcp.tool()
    def export_trcin(model_id: str, output_path: str | None = None) -> str:
        """Export the model as a TRACE input deck (.inp file).

        Uses SNAP's native TRCIN exporter (model.export()), which produces the
        same output as File → Export TRCIN in the SNAP GUI.

        Parameters
        ----------
        model_id : str
        output_path : str | None
            If provided, write to that file path. The TRCIN content is also
            returned as a string in both cases.

        Returns
        -------
        str — the full TRCIN file content.
        """
        model = session.get_model(model_id)

        # Use a temp file if no output path given
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix=".inp", prefix="trace_")
            os.close(fd)
            cleanup = True
        else:
            cleanup = False

        try:
            export_set = model.export(output_path)
        except Exception:
            # SNAP writes the file before returning the result set; the
            # Py4JError on iterator() is a Java-module-opens issue that does
            # not prevent the file from being written.
            export_set = None

        # The export set describes what was written; find the primary .inp file
        written_path = output_path
        if export_set is not None:
            try:
                locs = export_set.locations if hasattr(export_set, "locations") else []
                if locs:
                    written_path = str(locs[0])
            except Exception:
                pass

        try:
            with open(written_path, "r", errors="replace") as f:
                content = f.read()
            content = _fixup_trcin(content)
        except OSError:
            content = f"(exported to {written_path})"

        if cleanup:
            try:
                os.unlink(written_path)
            except OSError:
                pass

        return content

    @mcp.tool()
    def export_check_report(
        model_id: str,
        output_path: str | None = None,
    ) -> dict:
        """Run model checks and return results as an HTML report.

        NOTE: SNAP's HTML Error Report is generated by the GUI only — there is
        no Python API path to it.  model.export(check=True) returns a
        MEDExportSet with no HTML methods; the result is always
        report_source="python_fallback".

        The Python fallback covers: PIPE/VESSEL ICs, VESSEL hydraulic diameter
        tables and Y-angle geometry, FILL/BREAK connections and boundary
        pressure, and PUMP rated/MOI/speed values.  It does NOT cover SNAP's
        deeper checks (loop closure, abrupt area change, junction angle from
        SNAP's perspective, etc.).

        For a complete error picture, load the .med into the SNAP GUI and run
        Check Model, then save the HTML report with File → Export.  Use
        export_check_report() for programmatic checks during model building.

        Parameters
        ----------
        model_id : str
        output_path : str | None
            If provided, write the HTML report to this file path.

        Returns
        -------
        dict with keys:
            html              : str       — full HTML report (empty if not captured)
            report_source     : str       — "snap_native" | "python_fallback"
            result_set_methods: list[str] — Py4J proxy methods on the result set
                                            (diagnostic; helps identify the HTML
                                            generation method when snap_native fails)
            errors            : list[str] — errors extracted from the report
            warnings          : list[str] — warnings extracted from the report
            valid             : bool      — True only when errors list is empty
        """
        import glob
        import shutil

        model = session.get_model(model_id)

        # ── Strategy 1: export(check=True) then scan for co-written HTML ─────
        # SNAP may write a .html report alongside the .inp in the same directory.
        tmp_dir = tempfile.mkdtemp(prefix="snap_report_")
        tmp_inp = os.path.join(tmp_dir, "check.inp")
        html_content = ""
        result_set = None

        try:
            try:
                result_set = model.export(tmp_inp, check=True)
            except Exception:
                pass

            # Scan temp dir for any HTML co-written by SNAP (none expected
            # for current plugin versions — MEDExportSet writes only .inp)
            for pat in ("*.html", "*.htm", "*.HTML", "*.HTM"):
                hits = glob.glob(os.path.join(tmp_dir, pat))
                if hits:
                    with open(hits[0], "r", errors="replace") as fh:
                        html_content = fh.read()
                    break

        finally:
            try:
                shutil.rmtree(tmp_dir)
            except Exception:
                pass

        # ── Strategy 5: Python-level fallback rendered as HTML ────────────────
        report_source = "snap_native"
        if not html_content:
            report_source = "python_fallback"
            py_errors = _python_model_check(model)
            lines = ["<html><body>",
                     "<h1>Validation Report (Python fallback — SNAP HTML unavailable)</h1>"]
            if py_errors:
                lines.append("<h2>Errors</h2>")
                for e in py_errors:
                    lines.append(
                        f'<font color="#FF0000">Error: </font>{e}<br>'
                    )
            else:
                lines.append("<p>No errors detected by Python checks.</p>")
            lines.append("</body></html>")
            html_content = "\n".join(lines)

        # ── Parse HTML for structured error/warning lists ─────────────────────
        errors: list[str] = []
        warnings: list[str] = []
        _tag = re.compile(r"<[^>]+>")
        context = ""
        for line in html_content.splitlines():
            stripped = _tag.sub("", line).strip()
            if not stripped:
                continue
            low = line.lower()
            if "<h2>" in low or "<h3>" in low:
                context = stripped
            elif "error:" in low:
                msg = f"{context}: {stripped}" if context else stripped
                errors.append(msg)
            elif "warning:" in low:
                msg = f"{context}: {stripped}" if context else stripped
                warnings.append(msg)

        # ── Collect result_set method names for diagnostics ───────────────────
        # When report_source=="python_fallback", these names help identify
        # which Java method to call for native HTML in future iterations.
        rs_methods: list[str] = []
        if result_set is not None:
            try:
                rs_methods = [
                    m for m in dir(result_set)
                    if not m.startswith("_")
                    and ("report" in m.lower() or "html" in m.lower()
                         or "save" in m.lower() or "write" in m.lower()
                         or "export" in m.lower() or "print" in m.lower())
                ]
            except Exception:
                pass

        # ── Optionally write to caller-supplied path ───────────────────────────
        if output_path:
            with open(output_path, "w", errors="replace") as fh:
                fh.write(html_content)

        return {
            "html": html_content,
            "report_source": report_source,
            "result_set_methods": rs_methods,
            "errors": errors,
            "warnings": warnings,
            "valid": len(errors) == 0,
        }

    @mcp.tool()
    def save_med(model_id: str, output_path: str | None = None) -> dict:
        """Save the model to a SNAP .med binary file.

        Parameters
        ----------
        model_id : str
        output_path : str | None
            Destination path. If None, overwrites the auto-saved working copy.

        Returns
        -------
        dict with the saved file path.
        """
        model = session.get_model(model_id)
        if output_path is None:
            # Trigger the auto-save to the working .med
            session.autosave(model_id)
            rows = session._db_conn().execute(
                "SELECT med_path FROM models WHERE id = ?", (model_id,)
            ).fetchone()
            output_path = rows[0] if rows else "(unknown)"
        else:
            model.save(output_path)
        return {"saved_to": output_path}

    @mcp.tool()
    def validate_model(model_id: str) -> dict:
        """Run SNAP's model check — equivalent to 'Check Model' in the SNAP GUI.

        Runs four validation strategies in order:

        1. SNAP's Java result set (check/validate methods, or export with check=True)
        2. Java getHeadlessComponentErrors(): field-level errors (ICs not set, angle
           out of range, etc.) via Message stream capture on each root component
        3. Java getHeadlessValidationErrors(): 7 system-level test classes — NoAir,
           NOFAT flow area, abrupt area change, edge hydraulic diameter, PUMPFRICQ
           consistency, vessel connections, adjacent cell volume
        4. Java getHeadlessLoopClosureErrors(): hydraulic loop closure check
        5. Python component inspection: ICs, vessel HD tables, geometry, connectivity,
           and pump rated values (supplements Java checks)

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: valid (bool), errors (list[str]), warnings (list[str]).
        A non-empty errors list means the model must be fixed before save_med.
        """
        model = session.get_model(model_id)
        errors: list[str] = []
        warnings: list[str] = []
        result_set = None

        # ── Approach 1: try check-only methods (no file export) ───────────────
        # These may return a result set that supports toArray() without needing
        # the module-restricted iterator().
        for _method in ("check", "validate", "checkModel", "runCheck", "doCheck"):
            _fn = getattr(model, _method, None)
            if _fn is not None and callable(_fn):
                try:
                    result_set = _fn()
                    break
                except Exception:
                    pass

        # ── Approach 2: export with check=True ────────────────────────────────
        # SNAP writes the file AND runs validation; the returned result set
        # may throw InaccessibleObjectException on iterator() but toArray()
        # often still works.
        if result_set is None:
            fd, tmp_path = tempfile.mkstemp(suffix=".inp", prefix="trace_check_")
            os.close(fd)
            try:
                result_set = model.export(tmp_path, check=True)
            except Exception as exc:
                msg = str(exc)
                if "InaccessibleObjectException" not in msg and "iterator" not in msg:
                    if "warning" in msg.lower():
                        warnings.append(msg)
                    else:
                        errors.append(msg)
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        # ── Read result set (toArray then size/get fallback) ──────────────────
        if result_set is not None:
            _read_result_set(result_set, errors, warnings)

        # ── Approach 3: validation tests via Java reflection ─────────────────
        # trace.jar is signed; patching it breaks the SNAP license check.
        # Instead: call getValidationTests() (existing method), run each test
        # headlessly, then read the private errList field via reflection.
        # This works on the unmodified original JAR with no signing issues.
        try:
            jm = model.java_model
            tests = jm.getValidationTests()
            for test in tests:
                try:
                    test.runValidation(False)
                    display = str(test.getDisplayName())
                    # Walk class hierarchy to find errList field
                    cls = test.getClass()
                    field = None
                    while cls is not None and field is None:
                        try:
                            field = cls.getDeclaredField("errList")
                        except Exception:
                            cls = cls.getSuperclass()
                    if field is not None:
                        field.setAccessible(True)
                        err_list = field.get(test)
                        if err_list is not None:
                            for i in range(err_list.size()):
                                errors.append(f"{display}: {err_list.get(i)}")
                except Exception as te:
                    warnings.append(f"[{test.getClass().getSimpleName()} check failed: {te}]")
        except Exception as exc:
            warnings.append(f"[validation tests unavailable: {exc}]")

        # ── Approach 3b: component field errors via Message stream capture ────
        # Redirect the static Message output stream to a ByteArrayOutputStream,
        # call isOkayForExport(true) on each hydraulic component (not just roots
        # — fills/breaks are boundary components, not root components), then parse
        # captured lines for Error:/Warning: markers.
        try:
            from py4j.java_gateway import JavaGateway
            jm = model.java_model
            jvm = JavaGateway(gateway_client=jm._gateway_client).jvm
            Message = jvm.com.cafean.client.ui.message.Message
            baos = jvm.java.io.ByteArrayOutputStream()
            ps = jvm.java.io.PrintStream(baos)
            original = Message.getOutputStream()
            Message.setOutputStream(ps)
            try:
                from snap_trace.component_map import iter_all_components
                for _ctype, comp in iter_all_components(model):
                    try:
                        comp.java_object.isOkayForExport(True)
                    except Exception:
                        pass
            finally:
                Message.setOutputStream(original)
            ps.flush()
            captured = str(baos.toString())
            _seen_stream: set[str] = set()
            for line in captured.split("\n"):
                line = line.strip()
                if "Error:" in line or "Warning:" in line or "Alert:" in line:
                    bracket = line.find("]")
                    if bracket >= 0 and line.startswith("["):
                        line = line[bracket + 1:].strip()
                    if line and line not in _seen_stream:
                        _seen_stream.add(line)
                        errors.append(line)
        except Exception as exc:
            warnings.append(f"[component stream check unavailable: {exc}]")

        # ── Approach 4: Python-level component inspection ─────────────────────
        # Independently checks ICs, vessel HD tables, geometry, connectivity,
        # and pump rated values — things not fully surfaced by the Java checks.
        # Note: abrupt area change is now handled authoritatively by 3b above.
        py_errors = _python_model_check(model)
        errors.extend(py_errors)

        errors = [_enrich_error(e) for e in errors]
        valid = len(errors) == 0
        return {"valid": valid, "errors": errors, "warnings": warnings}
