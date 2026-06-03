"""Model-level tools: status, create, import, open, list, close."""

from __future__ import annotations
import uuid
import logging

from snap_relap import session as _session
from snap_relap.component_map import find_component

log = logging.getLogger(__name__)


def _patch_junction_connections(model, path: str):
    """Parse RELAP5 input deck to extract junction connection cards and apply them to the model."""
    connections = {}  # j_cc -> (inlet, outlet)
    
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("*"):
                    continue
                
                if "*" in line:
                    line = line.split("*")[0].strip()
                    
                tokens = line.split()
                if len(tokens) < 3:
                    continue
                    
                card_str = tokens[0]
                if not card_str.isdigit():
                    continue
                    
                card = int(card_str)
                # CCC0101 card where CCC is component number
                if card % 10000 == 101:
                    j_cc = card // 10000
                    inlet = tokens[1]
                    outlet = tokens[2]
                    
                    if inlet.isdigit() and outlet.isdigit():
                        connections[j_cc] = (inlet, outlet)
    except Exception as exc:
        log.warning(f"Could not read/parse RELAP input file for connections: {exc}")
        return

    # Wire them up in the model
    for j_cc, (inlet, outlet) in connections.items():
        try:
            ctype, comp = find_component(model, j_cc)
            if comp is not None and ctype in ("SINGLE_JUNCTION", "TIME_DEPENDENT_JUNCTION", "VALVE", "PUMP"):
                comp.inlet = inlet
                comp.outlet = outlet
                log.info(f"Patched connection for {ctype} {j_cc}: {inlet} -> {outlet}")
        except Exception as exc:
            log.warning(f"Could not patch connection for junction {j_cc}: {exc}")


def register_model_tools(mcp) -> None:

    @mcp.tool()
    def relap_status() -> dict:
        """Check that the RELAP SNAP plugin is loaded and return its version.

        Returns
        -------
        dict with keys: plugin_loaded (bool), version (str | None),
                        open_models (list[str])
        """
        try:
            import snap.codes.relap as _rl  # noqa: F401
            import snap.utils.version as _ver
            version = str(_ver.get_plugin_version("relap5.jar") or _ver.get_plugin_version("relap.jar"))
        except Exception as exc:
            return {"plugin_loaded": False, "error": str(exc), "open_models": []}

        return {
            "plugin_loaded": True,
            "version": version,
            "open_models": _session.list_ids(),
        }

    @mcp.tool()
    def create_model(code_version: str = "MOD3.3") -> dict:
        """Create a new empty RELAP model session.

        Parameters
        ----------
        code_version : str
            RELAP5 code version (e.g. "MOD3.3").

        Returns
        -------
        dict with keys: model_id (str), status (str), code_version (str)
        """
        import snap.codes.relap as _rl

        try:
            model = _rl.new_model(code_version)
        except Exception as exc:
            return {"model_id": None, "status": "error", "error": str(exc)}

        if model is None:
            return {"model_id": None, "status": "error", "error": "new_model returned None"}

        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok", "code_version": code_version}

    @mcp.tool()
    def import_relap(path: str) -> dict:
        """Import a RELAP5 ASCII input file (.inp) and open it as a model session.

        Parameters
        ----------
        path : str
            Full path to the RELAP5 input file.

        Returns
        -------
        dict with keys: model_id (str), status (str)
        """
        import snap.codes.relap as _rl

        try:
            model = _rl.import_relap5(path)
        except Exception as exc:
            return {"model_id": None, "status": "error", "error": str(exc)}

        if model is None:
            return {
                "model_id": None,
                "status": "error",
                "error": f"import_relap5 returned None for path: {path}",
            }

        # Post-import connection patching
        try:
            _patch_junction_connections(model, path)
        except Exception as exc:
            log.warning(f"Failed to post-patch junction connections: {exc}")

        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok"}

    @mcp.tool()
    def open_med_model(path: str) -> dict:
        """Open an existing RELAP .med file.

        Parameters
        ----------
        path : str
            Full path to the .med file.

        Returns
        -------
        dict with keys: model_id (str), status (str)
        """
        import snap.codes.relap as _rl

        try:
            model = _rl.open_model(path)
        except Exception as exc:
            return {"model_id": None, "status": "error", "error": str(exc)}

        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok"}

    @mcp.tool()
    def list_models() -> list[str]:
        """Return the IDs of all currently open RELAP model sessions."""
        return _session.list_ids()

    @mcp.tool()
    def close_model(model_id: str) -> dict:
        """Close an open RELAP model session and release its resources.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: status (str)
        """
        try:
            _session.get(model_id)
        except KeyError as exc:
            return {"status": "error", "error": str(exc)}
            
        _session.remove(model_id)
        return {"status": "ok", "model_id": model_id}

    @mcp.tool()
    def set_model_options(
        model_id: str,
        name: str,
        value: object,
    ) -> dict:
        """Set a property on the model options (such as timestep_table).

        Parameters
        ----------
        model_id : str
        name : str
            Property name (e.g. 'timestep_table').
        value : object
            Property value (scalar, list, or nested list of rows for table data).

        Returns
        -------
        dict with keys: status (str)
        """
        try:
            model = _session.get(model_id)
        except KeyError as exc:
            return {"status": "error", "error": str(exc)}

        opts = model.model_options()

        try:
            target_obj = opts
            prop_name = name
            if "." in name:
                parts = name.split(".")
                for part in parts[:-1]:
                    target_obj = getattr(target_obj, part)
                prop_name = parts[-1]

            table_prop = prop_name + "_table"
            if hasattr(target_obj, table_prop):
                prop_name = table_prop

            try:
                current_val = getattr(target_obj, prop_name)
            except Exception:
                current_val = None

            from snap.codes.properties import PropertyTable
            if isinstance(current_val, PropertyTable):
                if not isinstance(value, (list, tuple)):
                    return {"status": "error", "error": f"Property '{name}' is a table and expects a list of rows."}
                rows = []
                for r in value:
                    if isinstance(r, (list, tuple)):
                        rows.append(list(r))
                    else:
                        rows.append([r])
                try:
                    new_len = len(rows)
                    curr_len = len(current_val)
                    if new_len < curr_len:
                        try:
                            for idx in range(curr_len - 1, new_len - 1, -1):
                                current_val.remove_row(idx)
                        except Exception:
                            pass
                    current_val.read(rows)
                except Exception as exc:
                    return {"status": "error", "error": f"Failed to set table data: {exc}"}
            else:
                setattr(target_obj, prop_name, value)

            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

