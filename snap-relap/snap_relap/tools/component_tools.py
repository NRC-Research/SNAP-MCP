"""Component-level tools: add, list, get, set."""

from __future__ import annotations
import logging

from snap_relap import session as _session
from snap_relap.component_map import COMPONENT_MAP, _coerce_list, find_component

log = logging.getLogger(__name__)


def register_component_tools(mcp) -> None:

    @mcp.tool()
    def add_component(
        model_id: str,
        type: str,
        cc: int,
        properties: dict = None,
    ) -> dict:
        """Add a component to the RELAP model.

        Parameters
        ----------
        model_id : str
        type : str
            Component type (e.g. PIPE, SINGLE_VOLUME, TIME_DEPENDENT_VOLUME,
            SINGLE_JUNCTION, VALVE, HEAT_STRUCTURE, CONTROL_BLOCK).
        cc : int
            Component number / ID.
        properties : dict, optional
            Initial property values to set on the component.

        Returns
        -------
        dict with keys: status (str), component_number (int)
        """
        if properties is None:
            properties = {}

        model = _session.get(model_id)
        if type not in COMPONENT_MAP:
            return {
                "status": "error",
                "error": f"Unknown component type '{type}'. Supported: {list(COMPONENT_MAP.keys())}",
            }

        cfg = COMPONENT_MAP[type]
        creator_name = cfg["create"]
        creator = getattr(model, creator_name)

        try:
            # Dispatch to appropriate creation signatures
            if type == "PIPE":
                cells = int(properties.pop("cells", 1))
                comp = creator(cells, cc)
            elif type in ("SINGLE_JUNCTION", "TIME_DEPENDENT_JUNCTION", "VALVE"):
                area = float(properties.pop("area", 0.0))
                inlet = properties.pop("inlet", None)
                outlet = properties.pop("outlet", None)
                comp = creator(area, inlet, outlet, cc)
            elif type == "HEAT_STRUCTURE":
                geometry = int(properties.pop("geometry", 1))
                mesh_point_num = int(properties.pop("mesh_point_num", 2))
                comp = creator(geometry, mesh_point_num, cc)
            elif type == "CONTROL_BLOCK":
                cb_type = properties.pop("cb_type", "sum")
                comp = creator(cc, cb_type=cb_type)
            else:
                # No special signature
                comp = creator(cc)
        except Exception as exc:
            return {"status": "error", "error": f"Failed to create component: {exc}"}

        # Apply remaining properties
        warnings = []
        for k, v in properties.items():
            try:
                # Attempt to resolve enum strings (e.g., "ValveTypeSel.Servo_Valve")
                if isinstance(v, str) and "." in v:
                    try:
                        import importlib
                        mod_name, class_name_sel = v.split(".")
                        mod = importlib.import_module(f"snap.codes.relap.enums")
                        enum_class = getattr(mod, mod_name)
                        # Call the selector method
                        enum_val = getattr(enum_class, class_name_sel)()
                        v = enum_val
                    except Exception:
                        pass
                setattr(comp, k, v)
            except Exception as exc:
                warnings.append(f"Could not set property '{k}': {exc}")

        return {
            "status": "ok",
            "component_number": cc,
            "warnings": warnings if warnings else None,
        }

    @mcp.tool()
    def list_components(model_id: str) -> dict:
        """List all components currently in the RELAP model.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: components (list[dict])
        """
        model = _session.get(model_id)
        components = []

        for ctype, cfg in COMPONENT_MAP.items():
            try:
                getter = getattr(model, cfg["list"])
                items = _coerce_list(getter())
                for item in items:
                    cc = -1
                    name = ""
                    for attr in ("getCCnumber", "number", "getComponentNumber"):
                        try:
                            v = getattr(item, attr)
                            cc = int(v() if callable(v) else v)
                            break
                        except Exception:
                            pass
                    try:
                        name = str(item.name)
                    except Exception:
                        pass

                    components.append({
                        "type": ctype,
                        "number": cc,
                        "name": name,
                    })
            except Exception:
                pass

        return {"components": components}

    @mcp.tool()
    def get_component(model_id: str, cc: int) -> dict:
        """Inspect all properties of a specific component in the model.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.

        Returns
        -------
        dict with component properties
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, cc)

        if comp is None:
            return {"status": "error", "error": f"Component CC {cc} not found in model"}

        properties = {}
        # Scrape non-private, non-callable attributes
        for attr in dir(comp):
            if attr.startswith("_") or attr in ("java_object", "java_class", "getClass"):
                continue
            try:
                val = getattr(comp, attr)
                if callable(val):
                    continue
                # Normalize values
                if hasattr(val, "java_object"):
                    properties[attr] = str(val)
                else:
                    properties[attr] = val
            except Exception:
                pass

        return {
            "type": ctype,
            "number": cc,
            "properties": properties,
        }

    @mcp.tool()
    def set_component_property(
        model_id: str,
        cc: int,
        name: str,
        value: object,
    ) -> dict:
        """Set a property on an existing RELAP component.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.
        name : str
            Property name.
        value : object
            Property value (scalar, list, table data, or enum string).

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, cc)

        if comp is None:
            return {"status": "error", "error": f"Component CC {cc} not found in model"}

        try:
            # Handle dot path traversal (e.g. "geometry.mesh_source")
            target_obj = comp
            prop_name = name
            if "." in name:
                parts = name.split(".")
                for part in parts[:-1]:
                    target_obj = getattr(target_obj, part)
                prop_name = parts[-1]

            # Resolve enum strings if given
            if isinstance(value, str) and "." in value:
                try:
                    import importlib
                    mod_name, class_name_sel = value.split(".")
                    mod = importlib.import_module(f"snap.codes.relap.enums")
                    enum_class = getattr(mod, mod_name)
                    value = getattr(enum_class, class_name_sel)()
                except Exception:
                    pass

            setattr(target_obj, prop_name, value)
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}
