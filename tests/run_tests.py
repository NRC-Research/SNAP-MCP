"""
SNAP-MCP Test Runner

For each model in tests/suite/<Suite>/:
  1. Import via TRACE ASCII import (trace.import_ascii)
  2. Save as .med (model.save)
  3. Re-open the .med (trace.open_model)
  4. Extract component summary and topology
  5. Write tests/results/<Suite>/<stem>_summary.md
  6. Write tests/results/<Suite>/<stem>_prompt.md

Then write tests/test_report.md summarising all results.

Usage:
    SNAP_PYTHON_PATH=~/run-snap500/python \
        python tests/run_tests.py
"""
from __future__ import annotations

import os
import re
import sys
import tempfile
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap SNAP Python path
# ---------------------------------------------------------------------------
SNAP_PYTHON_PATH = os.environ.get(
    "SNAP_PYTHON_PATH", os.path.expanduser("~/run-snap500/python")
)
if SNAP_PYTHON_PATH not in sys.path:
    sys.path.insert(0, SNAP_PYTHON_PATH)

import snap.codes.trace as trace          # noqa: E402  (after path tweak)
import snap.model_editor as model_editor  # noqa: E402

SUITE_DIR = Path(__file__).parent / "suite"
RESULTS_DIR = Path(__file__).parent / "results"
MED_DIR = RESULTS_DIR / "_med_cache"

KEY_PROPS: dict[str, list[str]] = {
    "FILL":            ["pin", "tlin", "tvin", "flowin", "alpin", "inpvel", "ifty", "dxin", "volin"],
    "BREAK":           ["pin", "tin", "alpin", "isat", "ioff", "ibty", "dxin", "volin"],
    "PIPE":            ["cells", "fluid_segment", "epsw", "calculation_flag", "pipetype"],
    "PUMP":            ["name", "ipmpty", "apump", "vdpump", "riangd", "riangr"],
    "VALVE":           ["name", "ivty", "opnfrac", "cvtbl", "vopenf"],
    "TEE":             ["name"],
    "HEAT_STRUCTURE":  ["hscyl", "inner_radius", "th", "hgapo", "ichf", "iaxcnd",
                        "nofuelrod", "nfci", "nfcil", "dhtstrz", "rftn_table"],
    "VESSEL":          ["_nrsx", "_ntsx", "_nasx", "vess_type", "epsw"],
    "PLENUM":          ["name", "volin", "pin", "tlin"],
    "CONTAN_COMPARTMENT": ["name", "volin", "pin", "rml", "itrkl"],
    "SIGNAL_VARIABLE": ["name", "signal_type", "connection", "icn1"],
    "CONTROL_BLOCK":   ["name", "control_type", "cbgain", "cbxmin", "cbxmax",
                        "cbcon1", "cbcon2"],
    "POWER":           ["name"],
}


# ---------------------------------------------------------------------------
# SNAP initialisation (find_plugin triggers the JVM handshake)
# ---------------------------------------------------------------------------
def init_snap() -> None:
    print("Initialising SNAP/TRACE (this may take ~15 s) …", flush=True)
    model_editor.find_plugin("TRACE")
    print("SNAP ready.", flush=True)


# ---------------------------------------------------------------------------
# Component helpers (mirrors MCP component_tools logic)
# ---------------------------------------------------------------------------
def _cc(comp) -> int:
    try:
        return int(comp.java_object.getCCnumber())
    except Exception:
        return -1


def _name(comp) -> str:
    try:
        n = comp.name
        return str(n) if n else ""
    except Exception:
        return ""


def iter_all_components(model):
    """Yield (comp_type_str, component) for every component."""
    from snap_trace.component_map import COMPONENT_MAP
    for ctype, cfg in COMPONENT_MAP.items():
        try:
            getter = getattr(model, cfg["list"])
            raw = getter()
            if raw is None:
                continue
            items = raw if hasattr(raw, "__iter__") and not hasattr(raw, "java_object") else [raw]
            for comp in items:
                yield ctype, comp
        except Exception:
            pass


def get_key_props(comp_type: str, comp) -> dict:
    props = {}
    for attr in KEY_PROPS.get(comp_type, []):
        try:
            val = getattr(comp, attr)
            if callable(val):
                continue
            props[attr] = str(val)
        except Exception:
            pass
    return props


def get_connections(model) -> list[dict]:
    conns = []
    for comp_type, comp in iter_all_components(model):
        for face in ("inlet", "outlet", "side"):
            try:
                val = getattr(comp, face)
                if val is not None and str(val).strip() not in ("None", ""):
                    conns.append({
                        "component_number": _cc(comp),
                        "component_type": comp_type,
                        "face": face,
                        "connection": str(val),
                    })
            except Exception:
                pass
    return conns


def get_mesh_info(comp) -> dict:
    try:
        mesh = comp.mesh
        if mesh is None:
            return {}
        regions = mesh.material_regions
        layers = []
        for region in regions:
            layer: dict = {}
            try:
                mat = region.material
                mat_name = None
                for acc in ("name", "ctitle"):
                    try:
                        v = getattr(mat, acc)
                        if v and str(v).strip():
                            mat_name = str(v)
                            break
                    except Exception:
                        pass
                layer["material"] = mat_name or str(mat).strip() or None
            except Exception:
                pass
            try:
                layer["thickness_m"] = float(region.thickness)
            except Exception:
                pass
            try:
                layer["meshpoints"] = [float(p) for p in region.meshpoints]
            except Exception:
                pass
            layers.append(layer)
        return {"layers": layers} if layers else {}
    except Exception:
        return {}


def get_pipe_geometry(comp) -> dict:
    """Extract per-cell dx and per-edge hd from a PIPE's fluid segment."""
    result: dict = {}
    try:
        cells = comp.fluid_segment.cells
        dx_list = []
        for cell in cells:
            try:
                dx_list.append(float(cell.dx))
            except Exception:
                pass
        if dx_list:
            result["dx"] = dx_list
            result["total_length_m"] = sum(dx_list)
    except Exception:
        pass
    # hd lives on edges, not cells
    try:
        edges = comp.fluid_segment.edges
        hd_list = []
        for edge in edges:
            try:
                hd_list.append(float(edge.hd))
            except Exception:
                pass
        if hd_list:
            unique_hd = list(dict.fromkeys([round(v, 8) for v in hd_list]))
            result["hd"] = hd_list
            result["hd_uniform"] = unique_hd[0] if len(unique_hd) == 1 else None
    except Exception:
        pass
    return result


def get_hs_connections(comp) -> list[dict]:
    """Return per-cell inner/outer hydraulic connections for a HEAT_STRUCTURE.

    hcom.reference encodes both CC number and cell as: cc * 1000 + cell_index.
    Values <= 0 indicate no connection set.
    """
    connections: list[dict] = []
    try:
        for i, cell in enumerate(comp.cells):
            entry: dict = {"cell_index": i + 1}
            for face in ("inner", "outer"):
                try:
                    hcom = getattr(cell, face).hcom
                    ref = int(hcom.reference)
                    if ref > 0:
                        entry[face] = {"cc": ref // 1000, "cell": ref % 1000}
                except Exception:
                    pass
            if "inner" in entry or "outer" in entry:
                connections.append(entry)
    except Exception:
        pass
    return connections


# ---------------------------------------------------------------------------
# Summary & prompt generators
# ---------------------------------------------------------------------------
def build_summary(model_name: str, purpose: str,
                  components: list[dict], connections: list[dict],
                  details: list[dict]) -> str:
    lines = [f"# Model Summary: {model_name}\n"]
    if purpose:
        lines.append(f"**Purpose:** {purpose}\n\n")

    # Component table
    lines.append("## Components\n\n")
    lines.append("| Type | CC# | Name |\n|---|---|---|\n")
    for c in components:
        lines.append(f"| {c['type']} | {c['number']} | {c['name'] or '—'} |\n")

    # Connections
    if connections:
        lines.append("\n## Connections\n\n")
        lines.append("| Component | Face | Connected to |\n|---|---|---|\n")
        for cn in connections:
            lines.append(
                f"| {cn['component_type']} {cn['component_number']} "
                f"| {cn['face']} | {cn['connection']} |\n"
            )

    # Per-component key properties
    lines.append("\n## Key Properties\n")
    for d in details:
        lines.append(f"\n### {d['type']} {d['number']}\n")
        if d.get("props"):
            for k, v in d["props"].items():
                if v and v not in ("None", ""):
                    lines.append(f"- `{k}`: {v}\n")
        if d.get("mesh"):
            lines.append("- **Radial mesh layers:**\n")
            for i, layer in enumerate(d["mesh"].get("layers", []), 1):
                lines.append(f"  - Layer {i}: material={layer.get('material')}, "
                             f"thickness={layer.get('thickness_m', '?')} m, "
                             f"nodes={len(layer.get('meshpoints', []))}\n")
        if d.get("geometry"):
            geo = d["geometry"]
            if "total_length_m" in geo:
                lines.append(f"- **Total length:** {geo['total_length_m']} m\n")
            if "dx" in geo:
                lines.append(f"- **dx per cell:** {geo['dx']} m\n")
            hd = geo.get("hd_uniform")
            if hd is not None:
                lines.append(f"- **Hydraulic diameter:** {hd} m\n")
            elif geo.get("hd"):
                lines.append(f"- **hd per cell:** {geo['hd']} m\n")
        if d.get("hs_connections"):
            lines.append("- **HS-fluid connections (first 3 cells shown):**\n")
            for hsc in d["hs_connections"][:3]:
                parts = []
                if "inner" in hsc:
                    parts.append(f"inner→CC{hsc['inner']['cc']} cell {hsc['inner']['cell']}")
                if "outer" in hsc:
                    parts.append(f"outer→CC{hsc['outer']['cc']} cell {hsc['outer']['cell']}")
                lines.append(f"  - Cell {hsc['cell_index']}: {', '.join(parts)}\n")

    return "".join(lines)


def build_recipe(model_name: str, purpose: str,
                 components: list[dict], connections: list[dict],
                 details: list[dict]) -> str:
    """Generate a step-by-step tool-call recipe for exact model reconstruction."""
    lines = [
        f"# Reconstruction Prompt: {model_name}\n\n",
        "Use the snap-trace MCP tools to recreate the following TRACE model.\n",
        "Call `snap_status()` first to confirm the connection, "
        "then follow the steps below.\n\n",
    ]
    if purpose:
        lines.append(f"**Model purpose:** {purpose}\n\n")

    lines.append("## Step 1 — Create the model\n\n```\ncreate_model(")
    lines.append(f'"{model_name}")\n```\n\n')

    lines.append("## Step 2 — Add components\n\n")
    lines.append("Add the following components with `add_component()`. "
                 "Consult `get_component_schema(type)` before each call.\n\n")

    detail_map = {(d["type"], d["number"]): d for d in details}

    for c in components:
        ct, num = c["type"], c["number"]
        d = detail_map.get((ct, num), {})
        props = d.get("props", {})
        mesh = d.get("mesh", {})

        lines.append(f"### {ct} {num} ({c['name'] or 'unnamed'})\n\n")

        # Initializer hint for types that need one
        if ct == "PIPE":
            cells_str = props.get("cells", "")
            n_cells = len(cells_str.split(",")) if cells_str else "?"
            geo = d.get("geometry", {})
            length = geo.get("total_length_m", "<total length m>")
            hd = geo.get("hd_uniform")
            if hd is None and geo.get("hd"):
                hd = geo["hd"]
            hd_str = str(hd) if hd is not None else "<hydraulic diameter m>"
            lines.append(
                f"```\nadd_component(model_id, 'PIPE', {num}, {{}}, initializer={{\n"
                f'    "nsegs": {n_cells},\n'
                f'    "n_pipes": 1,\n'
                f'    "length": {length},\n'
                f'    "hd": {hd_str}\n'
                f"}})\n```\n"
            )
        elif ct == "HEAT_STRUCTURE":
            layers = mesh.get("layers", [])
            material = layers[0]["material"] if layers else "Material 8"
            inner_r = props.get("inner_radius", "?")
            n_radial = len(layers[0].get("meshpoints", [])) + 1 if layers else 9
            # Axial count and length from dhtstrz
            dhtstrz_str = props.get("dhtstrz", "")
            try:
                dhtstrz_vals = [float(x) for x in dhtstrz_str.strip("[]").split(",")]
                n_axial = len(dhtstrz_vals)
                hs_length = sum(dhtstrz_vals)
            except Exception:
                n_axial = "?"
                hs_length = "<total length m>"
            # Initial temp from first value in rftn_table
            rftn_str = props.get("rftn_table", "")
            try:
                temp = float(rftn_str.strip().split("\n")[0].strip("[]").split(",")[0])
            except Exception:
                temp = "<initial temperature K>"
            thickness = (layers[0].get("thickness_m") if layers else None) or props.get("th", "?")
            lines.append(
                f"```\nadd_component(model_id, 'HEAT_STRUCTURE', {num}, {{}}, initializer={{\n"
                f'    "axial": {n_axial},\n'
                f'    "radial": {n_radial},\n'
                f'    "length": {hs_length},\n'
                f'    "inner": {inner_r},\n'
                f'    "hsycl": "HeatStructureGeometry.CYLINDRICAL",\n'
                f'    "th": {thickness},\n'
                f'    "temp": {temp},\n'
                f'    "material": "{material}"\n'
                f"}})\n```\n"
            )
        elif ct in ("PUMP", "VALVE"):
            lines.append(
                f"```\nadd_component(model_id, '{ct}', {num}, {{}}, "
                f"initializer={{<see schema>}})\n```\n"
            )
        else:
            lines.append(f"```\nadd_component(model_id, '{ct}', {num}, {{}})\n```\n")

        # Key properties to set
        # fluid_segment is a display label that cannot be set via the MCP API (SNAP bug)
        UNSETTABLE = {"cells", "cells_enabled", "fluid_segment"}
        settable = {k: v for k, v in props.items()
                    if v and v not in ("None", "") and "enabled" not in k
                    and k not in UNSETTABLE}
        if settable:
            lines.append("\nSet properties:\n")
            for k, v in list(settable.items())[:12]:
                lines.append(f"- `{k}` = `{v}`\n")
        lines.append("\n")

    # Build lookup: cc → component_type, and vessel dims: cc → (nr, nt)
    cc_to_type = {c["number"]: c["type"] for c in components}
    vessel_dims: dict[int, tuple[int, int]] = {}
    for d in details:
        if d["type"] == "VESSEL":
            try:
                nr = int(d["props"].get("_nrsx", "1"))
            except Exception:
                nr = 1
            try:
                nt = int(d["props"].get("_ntsx", "1"))
            except Exception:
                nt = 1
            vessel_dims[d["number"]] = (nr, nt)

    # Connections — emit concrete connection calls
    if connections:
        lines.append("## Step 3 — Connect components\n\n")
        lines.append(
            "Use `connect_components()` for 1-D to 1-D connections, "
            "and `connect_pipe_to_vessel()` when the target is a VESSEL:\n\n"
        )
        lines.append("```\n")
        seen_pairs: set = set()
        for cn in connections:
            # Parse raw connection string: "('[JUN1] Inlet', 12, 1)" or "('', 8, 1)"
            raw = cn["connection"]
            try:
                tup = eval(raw)  # safe: only tuples of str/int from SNAP
                label, tgt_cc, tgt_cell = tup
                pair = tuple(sorted([cn["component_number"], tgt_cc]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                if cc_to_type.get(tgt_cc) == "VESSEL":
                    # Decompose flat cell index → (level, ring, sector)
                    nr, nt = vessel_dims.get(tgt_cc, (1, 1))
                    idx = tgt_cell - 1  # convert to 0-based
                    level  = idx // (nr * nt) + 1
                    planar = idx % (nr * nt)
                    ring   = planar // nt + 1
                    sector = planar % nt + 1
                    # Face label may be blank from imported model; default to standard
                    vessel_face = label if label and label not in ("[JUN1] Inlet", "[JUN2] Outlet") \
                        else "Positive Azimuthal"
                    lines.append(
                        f"connect_pipe_to_vessel(model_id, {cn['component_number']}, "
                        f'"{cn["face"]}", {tgt_cc}, '
                        f"{level}, vessel_ring={ring}, vessel_sector={sector}, "
                        f'vessel_face="{vessel_face}")\n'
                    )
                else:
                    if not label:
                        label = "[JUN1] Inlet"
                    lines.append(
                        f"connect_components(model_id, {cn['component_number']}, "
                        f'"{cn["face"]}", "{label}", {tgt_cc}, {tgt_cell})\n'
                    )
            except Exception:
                lines.append(f"# {cn['component_type']} {cn['component_number']} "
                             f"{cn['face']} → {raw}\n")
        lines.append("```\n")

    # HS-fluid coupling step — emit concrete connect_heat_structure calls
    hs_details = [d for d in details
                  if d["type"] == "HEAT_STRUCTURE" and d.get("hs_connections")]
    if hs_details:
        lines.append("\n## Step 3b — Wire heat structure surfaces to hydraulic components\n\n")
        lines.append("Use `connect_heat_structure()` for each (hs_cell, face) pair:\n\n")
        for d in hs_details:
            lines.append(f"**HS {d['number']}**\n\n```\n")
            for hsc in d["hs_connections"]:
                ci = hsc["cell_index"]
                for face in ("inner", "outer"):
                    if face in hsc:
                        cc = hsc[face]["cc"]
                        hcell = hsc[face]["cell"]
                        lines.append(
                            f"connect_heat_structure(model_id, {d['number']}, {ci}, "
                            f'"{face}", {cc}, {hcell})\n'
                        )
            lines.append("```\n\n")

    lines.append("\n## Step 4 — Validate and export\n\n")
    lines.append("```\nvalidate_model(model_id)\nexport_trcin(model_id)\n```\n")

    return "".join(lines)


def build_prompt(model_name: str, purpose: str,
                 components: list[dict], connections: list[dict],
                 details: list[dict]) -> str:
    """Generate a natural-language engineering prompt for the model.

    Describes WHAT the model represents and the key physical parameters,
    letting the AI figure out the tool calls from context.
    """
    detail_map = {(d["type"], d["number"]): d for d in details}

    # Classify components by role
    pipes   = [c for c in components if c["type"] == "PIPE"]
    fills   = [c for c in components if c["type"] == "FILL"]
    breaks  = [c for c in components if c["type"] == "BREAK"]
    hss     = [c for c in components if c["type"] == "HEAT_STRUCTURE"]
    pumps   = [c for c in components if c["type"] == "PUMP"]
    valves  = [c for c in components if c["type"] == "VALVE"]
    tees    = [c for c in components if c["type"] == "TEE"]
    others  = [c for c in components
                if c["type"] not in
                {"PIPE","FILL","BREAK","HEAT_STRUCTURE","PUMP","VALVE","TEE",
                 "SIGNAL_VARIABLE","TRIP","CONTROL_BLOCK"}]

    lines = [
        f"# TRACE Model: {model_name}\n\n",
        "Build this model using the snap-trace MCP tools. "
        "Start with `snap_status()` to confirm the connection, "
        "then `create_model()`. "
        "Use `get_component_schema()` before adding each new component type. "
        "Wire hydraulic junctions with `connect_components()`, "
        "heat structure surfaces with `connect_heat_structure()`, "
        "then finish with `validate_model()` and `export_trcin()`.\n\n",
    ]

    if purpose:
        lines.append(f"**Purpose:** {purpose}\n\n")

    # ── Hydraulic pipes ──────────────────────────────────────────────────────
    if pipes:
        lines.append("## Hydraulic pipes\n\n")
        for c in pipes:
            d = detail_map.get(("PIPE", c["number"]), {})
            props = d.get("props", {})
            geo   = d.get("geometry", {})
            label = c["name"].strip("$").strip() if c["name"] else f"pipe {c['number']}"
            n     = geo.get("total_length_m", "?")
            ncells = props.get("cells", "")
            ncells = len(ncells.split(",")) if ncells else "?"
            hd_u  = geo.get("hd_uniform")
            hd_str = f"{hd_u*1000:.1f} mm" if hd_u else "see geometry"
            epsw  = props.get("epsw", "")
            epsw_str = f", wall roughness {epsw} m" if epsw and epsw != "0.0" else ""
            lines.append(
                f"**CC {c['number']} — {label}**: "
                f"{ncells}-cell pipe, {n} m long, {hd_str} hydraulic diameter{epsw_str}.\n\n"
            )

    # ── Boundary conditions ──────────────────────────────────────────────────
    if fills or breaks:
        lines.append("## Boundary conditions\n\n")
        for c in fills:
            d = detail_map.get(("FILL", c["number"]), {})
            props = d.get("props", {})
            label = c["name"].strip("$").strip() if c["name"] else f"fill {c['number']}"
            pin   = props.get("pin", "?")
            tlin  = props.get("tlin", "?")
            flow  = props.get("flowin", "?")
            ifty  = props.get("ifty", "")
            flow_type = "constant mass flow" if "Constant_Mass_Flow" in ifty else ifty
            lines.append(
                f"**CC {c['number']} — {label}** (FILL): "
                f"{flow_type}, {flow} kg/s, {pin} Pa, {tlin} K inlet temperature.\n\n"
            )
        for c in breaks:
            d = detail_map.get(("BREAK", c["number"]), {})
            props = d.get("props", {})
            label = c["name"].strip("$").strip() if c["name"] else f"break {c['number']}"
            pin   = props.get("pin", "?")
            tin   = props.get("tin", "?")
            lines.append(
                f"**CC {c['number']} — {label}** (BREAK): "
                f"pressure boundary at {pin} Pa, {tin} K.\n\n"
            )

    # ── Pumps / valves / tees ────────────────────────────────────────────────
    for c in pumps:
        d = detail_map.get(("PUMP", c["number"]), {})
        props = d.get("props", {})
        label = c["name"].strip("$").strip() if c["name"] else f"pump {c['number']}"
        lines.append(
            f"**CC {c['number']} — {label}** (PUMP): "
            f"see original model for pump curve and geometry.\n\n"
        )
    for c in valves:
        label = c["name"].strip("$").strip() if c["name"] else f"valve {c['number']}"
        lines.append(f"**CC {c['number']} — {label}** (VALVE): see original model.\n\n")
    for c in tees:
        label = c["name"].strip("$").strip() if c["name"] else f"tee {c['number']}"
        lines.append(f"**CC {c['number']} — {label}** (TEE): three-way junction.\n\n")
    for c in others:
        lines.append(f"**CC {c['number']}** ({c['type']}): see original model.\n\n")

    # ── Heat structures ──────────────────────────────────────────────────────
    if hss:
        lines.append("## Heat structures\n\n")
        for c in hss:
            d = detail_map.get(("HEAT_STRUCTURE", c["number"]), {})
            props = d.get("props", {})
            mesh  = d.get("mesh", {})
            hsc   = d.get("hs_connections", [])
            label = c["name"].strip("$").strip() if c["name"] else f"HS {c['number']}"
            layers = mesh.get("layers", [])
            mat    = layers[0]["material"] if layers else props.get("material", "?")
            inner_r = props.get("inner_radius", "?")
            th      = props.get("th", "?")
            hscyl   = props.get("hscyl", "1")
            geo_str = "cylindrical" if str(hscyl) == "1" else "slab"
            dhtstrz_str = props.get("dhtstrz", "")
            try:
                dz_vals = [float(x) for x in dhtstrz_str.strip("[]").split(",")]
                n_axial = len(dz_vals)
                hs_len  = sum(dz_vals)
                dz_desc = f"{n_axial} axial zone{'s' if n_axial != 1 else ''}, {hs_len} m total"
            except Exception:
                dz_desc = "see geometry"
            n_radial = len(layers[0].get("meshpoints", [])) + 1 if layers else "?"
            rftn_str = props.get("rftn_table", "")
            try:
                t0 = float(rftn_str.strip().split("\n")[0].strip("[]").split(",")[0])
                t0_str = f"{t0} K"
            except Exception:
                t0_str = "see model"
            lines.append(
                f"**CC {c['number']} — {label}** ({geo_str} heat structure): "
                f"{dz_desc}, {n_radial} radial mesh points, "
                f"inner radius {inner_r} m, wall thickness {th} m, "
                f"material {mat}, initialized at {t0_str}.\n"
            )
            if hsc:
                # Summarise coupling concisely
                inner_pairs = [(h["inner"]["cc"], h["inner"]["cell"])
                               for h in hsc if "inner" in h]
                outer_pairs = [(h["outer"]["cc"], h["outer"]["cell"])
                               for h in hsc if "outer" in h]
                def fmt_pairs(pairs):
                    if not pairs: return "none"
                    cc = pairs[0][0]
                    cells = [str(p[1]) for p in pairs]
                    return f"CC {cc} cells {', '.join(cells)}"
                lines.append(
                    f"  - Inner surface → {fmt_pairs(inner_pairs)}\n"
                    f"  - Outer surface → {fmt_pairs(outer_pairs)}\n"
                )
            lines.append("\n")

    # ── Hydraulic topology ───────────────────────────────────────────────────
    if connections:
        lines.append("## Flow topology\n\n")
        seen_pairs: set = set()
        topo_lines = []
        for cn in connections:
            raw = cn["connection"]
            try:
                tup = eval(raw)
                _, tgt_cc, tgt_cell = tup
                pair = tuple(sorted([cn["component_number"], tgt_cc]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    src_label = next(
                        (c["name"].strip("$").strip() or str(c["number"])
                         for c in components if c["number"] == cn["component_number"]),
                        str(cn["component_number"])
                    )
                    tgt_label = next(
                        (c["name"].strip("$").strip() or str(c["number"])
                         for c in components if c["number"] == tgt_cc),
                        str(tgt_cc)
                    )
                    topo_lines.append(
                        f"- CC {cn['component_number']} ({src_label}) "
                        f"**{cn['face']}** → CC {tgt_cc} ({tgt_label}), cell {tgt_cell}\n"
                    )
            except Exception:
                pass
        lines.extend(topo_lines)
        lines.append("\n")

    # ── Component numbers reference ──────────────────────────────────────────
    lines.append("## Component number reference\n\n")
    lines.append("| CC | Type | Name |\n|---|---|---|\n")
    for c in components:
        label = c["name"].strip("$").strip() if c["name"] else "unnamed"
        lines.append(f"| {c['number']} | {c['type']} | {label} |\n")
    lines.append("\n")

    return "".join(lines)


# ---------------------------------------------------------------------------
# Per-model runner
# ---------------------------------------------------------------------------
def run_model(inp_path: Path, suite: str, results_suite_dir: Path) -> dict:
    stem = inp_path.stem
    result = {
        "suite": suite,
        "file": inp_path.name,
        "stem": stem,
        "import_ok": False,
        "save_ok": False,
        "reopen_ok": False,
        "component_count": 0,
        "components": [],
        "error": None,
    }

    med_path = MED_DIR / f"{stem}.med"

    try:
        # 1. Import ASCII
        print(f"  importing {inp_path.name} …", end=" ", flush=True)
        model = trace.import_ascii(str(inp_path))
        result["import_ok"] = True

        # 2. Save as MED
        model.save(str(med_path))
        result["save_ok"] = True
        model.close()

        # 3. Re-open MED
        model2 = trace.open_model(str(med_path))
        result["reopen_ok"] = True
        print("ok", flush=True)

        # 4. Extract components
        components = []
        details = []
        for comp_type, comp in iter_all_components(model2):
            num = _cc(comp)
            name = _name(comp)
            components.append({"type": comp_type, "number": num, "name": name})
            props = get_key_props(comp_type, comp)
            mesh = get_mesh_info(comp) if comp_type == "HEAT_STRUCTURE" else {}
            geometry = get_pipe_geometry(comp) if comp_type == "PIPE" else {}
            hs_connections = get_hs_connections(comp) if comp_type == "HEAT_STRUCTURE" else []
            details.append({"type": comp_type, "number": num, "name": name,
                            "props": props, "mesh": mesh,
                            "geometry": geometry, "hs_connections": hs_connections})

        result["component_count"] = len(components)
        result["components"] = components

        # 5. Connections
        connections = get_connections(model2)

        # Read purpose from XML header
        raw = inp_path.read_text(errors="replace")[:3000]
        purpose_m = re.search(r"<Purpose>(.*?)</Purpose>", raw, re.DOTALL)
        purpose = purpose_m.group(1).strip() if purpose_m else ""

        # 6. Write summary
        summary_md = build_summary(stem, purpose, components, connections, details)
        (results_suite_dir / f"{stem}_summary.md").write_text(summary_md)

        # 7. Write recipe (detailed tool-call guide) and natural-language prompt
        recipe_md = build_recipe(stem, purpose, components, connections, details)
        (results_suite_dir / f"{stem}_recipe.md").write_text(recipe_md)
        prompt_md = build_prompt(stem, purpose, components, connections, details)
        (results_suite_dir / f"{stem}_prompt.md").write_text(prompt_md)

    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
        print(f"FAILED — {result['error']}", flush=True)
        if result["import_ok"]:
            traceback.print_exc()

    return result


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------
def write_report(all_results: list[dict]) -> None:
    lines = ["# SNAP-MCP Test Report\n\n"]
    lines.append(f"Models tested: {len(all_results)}\n\n")

    pass_count = sum(1 for r in all_results if r["reopen_ok"])
    import_fail = sum(1 for r in all_results if not r["import_ok"])
    save_fail = sum(1 for r in all_results if r["import_ok"] and not r["save_ok"])
    reopen_fail = sum(1 for r in all_results if r["save_ok"] and not r["reopen_ok"])

    lines.append("## Summary\n\n")
    lines.append(f"| Phase | Passed | Failed |\n|---|---|---|\n")
    lines.append(f"| Import (ASCII → SNAP) | {len(all_results)-import_fail} | {import_fail} |\n")
    lines.append(f"| Save (.med) | {len(all_results)-import_fail-save_fail} | {save_fail} |\n")
    lines.append(f"| Re-open (.med) | {pass_count} | {reopen_fail} |\n")
    lines.append(f"| **End-to-end** | **{pass_count}** | **{len(all_results)-pass_count}** |\n")
    lines.append("\n")

    # Per-suite breakdown
    suites = sorted({r["suite"] for r in all_results})
    lines.append("## Results by Suite\n\n")
    for suite in suites:
        suite_results = [r for r in all_results if r["suite"] == suite]
        lines.append(f"### {suite}\n\n")
        lines.append("| Model | Import | Save | Re-open | Components | Notes |\n")
        lines.append("|---|---|---|---|---|---|\n")
        for r in suite_results:
            imp = "✓" if r["import_ok"] else "✗"
            sav = "✓" if r["save_ok"] else "✗"
            rop = "✓" if r["reopen_ok"] else "✗"
            note = r["error"] or ""
            if len(note) > 80:
                note = note[:77] + "…"
            lines.append(
                f"| [{r['file']}](suite/{suite}/{r['file']}) "
                f"| {imp} | {sav} | {rop} "
                f"| {r['component_count']} "
                f"| {note} |\n"
            )
        lines.append("\n")

    # Component type inventory
    lines.append("## Component Type Coverage\n\n")
    from collections import Counter
    type_counts: Counter = Counter()
    for r in all_results:
        for c in r.get("components", []):
            type_counts[c["type"]] += 1
    lines.append("| Component Type | Total instances across test suite |\n|---|---|\n")
    for ctype, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {ctype} | {cnt} |\n")
    lines.append("\n")

    # Failures detail
    failures = [r for r in all_results if not r["reopen_ok"]]
    if failures:
        lines.append("## Failure Details\n\n")
        for r in failures:
            lines.append(f"**{r['file']}** ({r['suite']})\n\n")
            lines.append(f"```\n{r['error']}\n```\n\n")

    lines.append("## Prompt Files\n\n")
    lines.append("Reconstruction prompts are saved alongside summaries in `tests/results/`.\n")
    lines.append("Each prompt is a self-contained instruction for an AI using the "
                 "snap-trace MCP to recreate the model.\n")

    report_path = Path(__file__).parent / "test_report.md"
    report_path.write_text("".join(lines))
    print(f"\nReport written to {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    init_snap()
    MED_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)

    all_results: list[dict] = []

    for suite_dir in sorted(SUITE_DIR.iterdir()):
        if not suite_dir.is_dir():
            continue
        suite = suite_dir.name
        results_suite = RESULTS_DIR / suite
        results_suite.mkdir(exist_ok=True)

        print(f"\n=== Suite: {suite} ===")
        for inp in sorted(suite_dir.glob("*.inp")):
            result = run_model(inp, suite, results_suite)
            all_results.append(result)

    write_report(all_results)
    print("\nDone.")


if __name__ == "__main__":
    main()
