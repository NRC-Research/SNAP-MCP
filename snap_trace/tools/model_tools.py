"""MCP tools: model lifecycle (create, open, import, list, status)."""
from __future__ import annotations

from pathlib import Path

import snap_trace.snap_env as snap_env
import snap_trace.session as session

_DEFAULT_VERSION = snap_env.SNAP_TRACE_TARGET_VERSION


def _resolve_path(tool: str, canonical: str, primary: str, alias: str) -> str:
    """Return the file path from either the canonical parameter or 'path'.

    Callers reliably guess 'path' for a tool whose parameter is actually
    'med_file_path' or 'trcin_path'. Without an alias that guess surfaces as a
    schema validation error naming a field the caller did not use, which reads
    as "the tool is broken" rather than "rename the argument" — and an agent
    that cannot see the fix simply retries the same call.

    Raises on neither-given and on both-given-and-different, so a genuine
    mistake is still reported rather than silently resolved.
    """
    primary, alias = (primary or "").strip(), (alias or "").strip()
    if primary and alias and primary != alias:
        raise ValueError(
            f"{tool}: '{canonical}' and 'path' were both given but differ "
            f"({primary!r} vs {alias!r}). Pass only one."
        )
    resolved = primary or alias
    if not resolved:
        raise ValueError(
            f"{tool}: a file path is required — pass '{canonical}' "
            f"(or its alias 'path')."
        )
    return resolved


def _namelist_value(prop):
    """Unwrap a namelist property to a JSON-safe value.

    Namelist properties are not uniform: ielv and nfrc1 carry a plain int on
    .value, while nvgrav carries an enum object (NLNvgravSel).  Try int first,
    then the enum's own int-ish attributes, and fall back to str() rather than
    returning an unserializable handle.
    """
    try:
        raw = prop.value
    except AttributeError:
        raw = prop

    if isinstance(raw, bool) or raw is None:
        return raw
    if isinstance(raw, (int, float, str)):
        return raw

    # Enum-valued option: prefer a numeric code, keep the label alongside it.
    for attr in ("value", "ordinal", "code"):
        try:
            inner = getattr(raw, attr)
            if isinstance(inner, (int, float)):
                return {"code": inner, "label": str(raw)}
        except Exception:
            pass
    return str(raw)


def register(mcp):

    @mcp.tool()
    def snap_status() -> dict:
        """Return the current status of the SNAP/TRACE connection.

        Call this first if you are unsure whether SNAP has finished
        initializing. 'ready: true' means all tools are usable.
        'initializing: true' means MEBatch is still starting up (wait ~15 s).

        Returns snap_plugin_version (the TRACE plugin version SNAP was built
        against) and target_trace_version (the TRACE binary version you are
        exporting for, set via SNAP_TRACE_TARGET_VERSION env var).  Export
        fixups are applied based on target_trace_version.
        """
        return snap_env.status()

    @mcp.tool()
    def get_model_options(model_id: str, names: list[str] = None) -> dict:
        """Return TRACE namelist options that change how a model is interpreted.

        Several model-wide namelist flags silently change what other values
        mean, or whether they can be edited at all.  Reading a component
        property without knowing these can lead to a confidently wrong
        conclusion, so check here first.

        Reported by default:
          ielv   — elevation option, and the one that governs GRAV:
                     0 = input gravity terms. Edge GRAV/angle are user-editable
                         (this is the TRACE default when ielv is absent).
                     1 = input cell elevations. SNAP derives GRAV from them and
                         locks the Orientation/Angle/Grav columns read-only.
                     2 = cell elevation change. The Grav column is removed from
                         the UI entirely.
          nvgrav — 3-D vessel orientation vs. the gravity vector
                   (0 = z-direction, 1 = explicitly input).
          nfrc1  — friction-correlation option; decides whether the reverse
                   K-factor (kfacr) participates.
          nfrc3  — additive friction option.

        Each entry reports 'value' plus 'enabled'.  Treat 'enabled' with care:
        it is True even on a brand-new model sitting at its default, so it does
        NOT mean "the user set this deliberately".  To distinguish a deliberate
        0 from an absent default, read the exported deck's &inopts block.

        Note SHELV (vessel stack elevation) is deliberately absent: it is a
        per-vessel component property, not a namelist option. Read it from the
        VESSEL component.

        Parameters
        ----------
        model_id : str
        names : list[str] | None
            Namelist option names to read (case-insensitive). Defaults to the
            GRAV/elevation-relevant set above. Unknown names are returned with
            an 'error' entry rather than raising, so one bad name in a batch
            does not lose the rest.

        Returns
        -------
        dict with model_id and 'options': {name: {value, enabled}}.
        """
        model = session.get_model(model_id)
        namelist = model.model_options().namelist

        wanted = names or ["ielv", "nvgrav", "nfrc1", "nfrc3"]
        out = {}
        for raw in wanted:
            key = str(raw).strip().lower()
            entry = {}
            try:
                prop = getattr(namelist, key)
            except AttributeError:
                available = sum(
                    1 for n in dir(namelist) if not n.startswith("_")
                )
                out[key] = {
                    "error": f"no namelist option named '{key}' "
                             f"({available} options exposed)"
                }
                continue

            entry["value"] = _namelist_value(prop)
            try:
                entry["enabled"] = bool(getattr(namelist, f"{key}_enabled"))
            except AttributeError:
                entry["enabled"] = None
            out[key] = entry

        return {"model_id": model_id, "options": out}

    @mcp.tool()
    def create_model(name: str, version: str = _DEFAULT_VERSION) -> dict:
        """Create a new, empty TRACE model.

        Parameters
        ----------
        name : str
            Human-readable name for the model.
        version : str
            TRACE code version string (e.g. "V5.0p5", "V5.0p9").
            Defaults to SNAP_TRACE_TARGET_VERSION env var (currently
            {_DEFAULT_VERSION}).

        Returns
        -------
        dict with model_id, name, version.
        The model_id is used in all subsequent tool calls.
        """
        snap_env.wait_ready()
        model_id, _ = session.create_model(name, version)
        return {"model_id": model_id, "name": name, "version": version}

    @mcp.tool()
    def list_models() -> list[dict]:
        """List all models tracked in this session (persisted across restarts)."""
        return session.list_models()

    @mcp.tool()
    def open_med_model(med_file_path: str = "", name: str = "",
                       path: str = "") -> dict:
        """Open an existing SNAP .med model file.

        Parameters
        ----------
        med_file_path : str
            Absolute path to the .med file.
        name : str
            Optional display name (defaults to the file stem).
        path : str
            Accepted alias for med_file_path. Give one or the other.

        Returns
        -------
        dict with model_id and component_count.
        """
        med_file_path = _resolve_path("open_med_model", "med_file_path",
                                      med_file_path, path)
        snap_env.wait_ready()
        import snap.codes.trace as trace
        model = trace.open_model(med_file_path)
        display = name or Path(med_file_path).stem
        model_id, _ = session.register_model(display, model, med_file_path)
        from snap_trace.component_map import iter_all_components
        count = len(iter_all_components(model))
        return {"model_id": model_id, "name": display, "component_count": count}

    @mcp.tool()
    def import_trcin(trcin_path: str = "", name: str = "",
                     version: str | None = None, path: str = "") -> dict:
        """Import an existing TRACE ASCII input deck (.inp / .trcin).

        Parameters
        ----------
        trcin_path : str
            Absolute path to the TRACE input file.
        name : str
            Optional display name.
        version : str | None
            Target TRACE version, or None for auto-detect.
        path : str
            Accepted alias for trcin_path. Give one or the other.

        Returns
        -------
        dict with model_id and component_count.
        """
        trcin_path = _resolve_path("import_trcin", "trcin_path",
                                   trcin_path, path)
        snap_env.wait_ready()
        import snap.codes.trace as trace
        model = trace.import_ascii(trcin_path, version)
        display = name or Path(trcin_path).stem
        model_id, _ = session.register_model(display, model, trcin_path)
        from snap_trace.component_map import iter_all_components
        count = len(iter_all_components(model))
        return {"model_id": model_id, "name": display, "component_count": count}
