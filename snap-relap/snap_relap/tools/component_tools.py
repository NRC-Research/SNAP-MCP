"""Component-level tools: add, list, get, set."""

from __future__ import annotations
import logging
import math
import importlib

from snap_relap import session as _session
from snap_relap.component_map import COMPONENT_MAP, _coerce_list, find_component

log = logging.getLogger(__name__)


def _set_pipe_geom_impl(comp, flow_area, length, hydraulic_diameter, vertical_angle, wall_roughness):
    """Internal helper to set PIPE geometry with scalar-to-list broadcasting."""
    cell_count = len(comp.x_length)
    junction_count = len(comp.flow_area)

    def broadcast(val, target_len):
        if hasattr(val, "__iter__") and not isinstance(val, (str, bytes)):
            val_list = list(val)
            if len(val_list) != target_len:
                if len(val_list) == target_len + 1:
                    return val_list[:target_len]
                raise ValueError(f"Length mismatch: got {len(val_list)}, expected {target_len}")
            return val_list
        return [val] * target_len

    comp.x_area = broadcast(flow_area, cell_count)
    comp.flow_area = broadcast(flow_area, junction_count)
    comp.x_length = broadcast(length, cell_count)
    comp.hydraulic_diameter = broadcast(hydraulic_diameter, junction_count)
    comp.vertical_angle = broadcast(vertical_angle, cell_count)
    comp.x_wall_roughness = broadcast(wall_roughness, cell_count)

    # Elevation auto-calculation
    try:
        dzx_list = []
        lengths = [float(x) for x in comp.x_length]
        angles = [float(x) for x in comp.vertical_angle]
        for l, a in zip(lengths, angles):
            dzx_list.append(l * math.sin(math.radians(a)))
        comp.elevation_change = dzx_list
    except Exception:
        pass


def _set_pipe_ics_impl(comp, pressure, temperature, void_fraction, ic_format):
    """Internal helper to set PIPE initial conditions with scalar-to-list broadcasting."""
    cell_count = len(comp.pressure)

    # Map ic_format to integer code
    fmt_map = {
        "Press_Liq_E_Vap_E_Void_Frac": 0,
        "Temp_Qual": 1,
        "Pressure_Quality": 2,
        "Press_Temp_Equilib_Cond": 3,
        "Temp_Qual_NC_Qual": 4,
        "Press_Liq_E_Vap_E_Vap_Void_Frac_NC_Qual": 5,
        "Press_Temp_Qual": 6,
    }
    
    ic_format_val = 3
    if isinstance(ic_format, int):
        ic_format_val = ic_format
    elif isinstance(ic_format, str):
        if ic_format.isdigit():
            ic_format_val = int(ic_format)
        else:
            ic_format_val = fmt_map.get(ic_format, 3)
    else:
        # Fallback for enum proxy object
        try:
            val_str = str(ic_format)
            for k, v in fmt_map.items():
                if k in val_str:
                    ic_format_val = v
                    break
        except Exception:
            pass

    def broadcast(val, count):
        if hasattr(val, "__len__") and not isinstance(val, (str, bytes)):
            if len(val) != count:
                raise ValueError(f"Length mismatch: got {len(val)}, expected {count}")
            return list(val)
        return [val] * count

    # Assign format FIRST so other properties become enabled if needed
    comp.ic_input_format = broadcast(ic_format_val, cell_count)

    # Try setting thermodynamic properties, skipping silently if they are disabled by the format
    try:
        comp.pressure = broadcast(pressure, cell_count)
    except Exception as exc:
        if "disabled" not in str(exc).lower():
            raise

    try:
        comp.temperature = broadcast(temperature, cell_count)
    except Exception as exc:
        if "disabled" not in str(exc).lower():
            raise

    try:
        comp.void_fraction = broadcast(void_fraction, cell_count)
    except Exception as exc:
        if "disabled" not in str(exc).lower():
            raise


def _enrich_enum_error(exc_msg: str) -> str:
    """Dynamically parses custom SNAP enum exceptions and lists acceptable selections."""
    marker = "snap.codes.relap.enums."
    if marker in exc_msg:
        try:
            start_idx = exc_msg.find(marker) + len(marker)
            end_idx = exc_msg.find("'", start_idx)
            if end_idx != -1:
                class_name = exc_msg[start_idx:end_idx]
                mod = importlib.import_module("snap.codes.relap.enums")
                enum_class = getattr(mod, class_name, None)
                if enum_class:
                    members = []
                    for name in dir(enum_class):
                        if name.startswith("_") or name in ("for_value", "from_value"):
                            continue
                        try:
                            attr = getattr(enum_class, name)
                            if callable(attr):
                                res = attr()
                                if isinstance(res, enum_class) or res.__class__.__name__ == enum_class.__name__:
                                    members.append(name)
                        except Exception:
                            pass
                    return f"Invalid enum value. Expected one of the values enumerated in '{class_name}': {', '.join(sorted(members))}"
        except Exception:
            pass
    return exc_msg


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
            Special creation-only properties depending on component type:
            - PIPE: 'cells' or 'num_cells' or 'numberOfCells' (int, default 1) - number of volumes.
            - SINGLE_JUNCTION / TIME_DEPENDENT_JUNCTION / VALVE:
                - 'area' or 'flow_area' (float, default 0.0) - flow area.
                - 'inlet' (str, optional) - source connection string.
                - 'outlet' (str, optional) - target connection string.
            - HEAT_STRUCTURE:
                - 'geometry' (int, default 1) - geometry number.
                - 'mesh_point_num' (int, default 2) - number of mesh points.
            - CONTROL_BLOCK:
                - 'cb_type' (str, default 'sum') - type of control block.

            Can also accept geometry/IC parameters at creation time for PIPEs:
            - 'flow_area', 'length', 'hydraulic_diameter', 'vertical_angle', 'wall_roughness',
              'pressure', 'temperature', 'void_fraction', 'ic_format'.

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

        # Extract geometry and IC properties for PIPE bulk setting
        pipe_geom = {}
        pipe_ics = {}
        if type == "PIPE":
            for k in ["flow_area", "length", "hydraulic_diameter", "vertical_angle", "wall_roughness"]:
                if k in properties:
                    pipe_geom[k] = properties.pop(k)
            for k in ["pressure", "temperature", "void_fraction", "ic_format"]:
                if k in properties:
                    pipe_ics[k] = properties.pop(k)

        try:
            # Dispatch to appropriate creation signatures
            if type == "PIPE":
                cells_val = properties.pop("cells", None)
                if cells_val is None:
                    cells_val = properties.pop("num_cells", None)
                if cells_val is None:
                    cells_val = properties.pop("numberOfCells", 1)
                cells = int(cells_val)
                comp = creator(cells, cc)
            elif type in ("SINGLE_JUNCTION", "TIME_DEPENDENT_JUNCTION", "VALVE"):
                area_val = properties.pop("area", None)
                if area_val is None:
                    area_val = properties.pop("flow_area", 0.0)
                area = float(area_val)
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

        # Apply PIPE bulk geometry and ICs if specified
        warnings = []
        if type == "PIPE" and (pipe_geom or pipe_ics):
            try:
                if pipe_geom:
                    flow_area = pipe_geom.get("flow_area", 0.0)
                    length = pipe_geom.get("length", 0.0)
                    hydraulic_diameter = pipe_geom.get("hydraulic_diameter", 0.0)
                    vertical_angle = pipe_geom.get("vertical_angle", 90.0)
                    wall_roughness = pipe_geom.get("wall_roughness", 4.6e-5)
                    _set_pipe_geom_impl(comp, flow_area, length, hydraulic_diameter, vertical_angle, wall_roughness)
                if pipe_ics:
                    pressure = pipe_ics.get("pressure", 1.013e5)
                    temperature = pipe_ics.get("temperature", 300.0)
                    void_fraction = pipe_ics.get("void_fraction", 0.0)
                    ic_format = pipe_ics.get("ic_format", 3)
                    _set_pipe_ics_impl(comp, pressure, temperature, void_fraction, ic_format)
            except Exception as exc:
                warnings.append(f"Failed to set initial PIPE geometry or ICs: {exc}")

        # Apply remaining properties
        for k, v in properties.items():
            try:
                # Check for name length limits
                if k == "name" and isinstance(v, str) and len(v) > 8:
                    warnings.append(f"Component name '{v}' truncated to 8 characters: '{v[:8]}'")
                    v = v[:8]

                # Attempt to resolve enum strings (e.g., "ValveTypeSel.Servo_Valve")
                if isinstance(v, str) and "." in v:
                    try:
                        mod_name, class_name_sel = v.split(".")
                        mod = importlib.import_module("snap.codes.relap.enums")
                        enum_class = getattr(mod, mod_name)
                        v = getattr(enum_class, class_name_sel)()
                    except Exception:
                        pass
                setattr(comp, k, v)
            except Exception as exc:
                enriched = _enrich_enum_error(str(exc))
                warnings.append(f"Could not set property '{k}': {enriched}")

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
    def get_component(
        model_id: str,
        cc: int,
        include_all: bool = False,
    ) -> dict:
        """Inspect all properties of a specific component in the model.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.
        include_all : bool, default False
            If True, returns all attributes including disabled fields and enabled flag status.
            By default, filters these out to reduce verbosity.

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
            if not include_all and attr.endswith("_enabled"):
                continue
            try:
                val = getattr(comp, attr)
                if callable(val):
                    continue
                # Normalize values
                if hasattr(val, "java_object"):
                    val_str = str(val)
                    if not include_all and ("disabled" in val_str.lower() or "ValueDisabledException" in val_str):
                        continue
                    properties[attr] = val_str
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

        Supports list broadcasting for array properties and dynamic enum validation.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.
        name : str
            Property name.
        value : object
            Property value (scalar, list, table data, or enum string like 'ValveTypeSel.Servo_Valve').

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, cc)

        if comp is None:
            return {"status": "error", "error": f"Component CC {cc} not found in model"}

        try:
            # Check for name length limit
            if name == "name" and isinstance(value, str) and len(value) > 8:
                log.warning(f"Component name '{value}' truncated to 8 characters.")
                value = value[:8]

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
                    mod_name, class_name_sel = value.split(".")
                    mod = importlib.import_module("snap.codes.relap.enums")
                    enum_class = getattr(mod, mod_name)
                    value = getattr(enum_class, class_name_sel)()
                except Exception:
                    pass

            # Scalar-to-list broadcasting logic
            try:
                current_val = getattr(target_obj, prop_name)
                if hasattr(current_val, "__len__") and not isinstance(current_val, (str, bytes, dict)):
                    if not hasattr(value, "__len__") or isinstance(value, (str, bytes)):
                        value = [value] * len(current_val)
            except Exception:
                pass

            setattr(target_obj, prop_name, value)

            # Auto-calculate elevation change (dzx) if vertical_angle or x_length is updated
            if prop_name == "vertical_angle":
                try:
                    if hasattr(target_obj, "x_length") and hasattr(target_obj, "dzx"):
                        l_val = getattr(target_obj, "x_length")
                        if hasattr(l_val, "__len__") and not isinstance(l_val, (str, bytes, dict)):
                            lengths = [float(x) for x in l_val]
                            angles = [float(x) for x in value]
                            target_obj.dzx = [l * math.sin(math.radians(a)) for l, a in zip(lengths, angles)]
                        else:
                            target_obj.dzx = float(l_val) * math.sin(math.radians(float(value)))
                except Exception:
                    pass
            elif prop_name == "x_length":
                try:
                    if hasattr(target_obj, "vertical_angle") and hasattr(target_obj, "dzx"):
                        a_val = getattr(target_obj, "vertical_angle")
                        if hasattr(a_val, "__len__") and not isinstance(a_val, (str, bytes, dict)):
                            lengths = [float(x) for x in value]
                            angles = [float(x) for x in a_val]
                            target_obj.dzx = [l * math.sin(math.radians(a)) for l, a in zip(lengths, angles)]
                        else:
                            target_obj.dzx = float(value) * math.sin(math.radians(float(a_val)))
                except Exception:
                    pass

            return {"status": "ok"}
        except Exception as exc:
            enriched = _enrich_enum_error(str(exc))
            return {"status": "error", "error": enriched}

    @mcp.tool()
    def list_enums(search: str = None) -> dict:
        """List available RELAP enum classes, optionally filtered by name substring.

        Parameters
        ----------
        search : str, optional
            Substring to filter enum class names (case-insensitive).
        """
        try:
            mod = importlib.import_module("snap.codes.relap.enums")
            names = [n for n in dir(mod) if not n.startswith("_") and isinstance(getattr(mod, n), type)]
            if search:
                search_lower = search.lower()
                names = [n for n in names if search_lower in n.lower()]
            return {"enums": sorted(names)}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to list enums: {exc}"}

    @mcp.tool()
    def get_enum_values(enum_name: str) -> dict:
        """Return all valid values/members of a specific RELAP enum class.

        Parameters
        ----------
        enum_name : str
            The name of the enum class (e.g. "TDVTFlagSel" or "ValveTypeSel").
        """
        try:
            mod = importlib.import_module("snap.codes.relap.enums")
            if not hasattr(mod, enum_name):
                return {"status": "error", "error": f"Enum class '{enum_name}' not found in snap.codes.relap.enums"}
            enum_class = getattr(mod, enum_name)
            
            members = []
            for name in dir(enum_class):
                if name.startswith("_") or name in ("for_value", "from_value"):
                    continue
                try:
                    attr = getattr(enum_class, name)
                    if callable(attr):
                        res = attr()
                        if isinstance(res, enum_class) or res.__class__.__name__ == enum_class.__name__:
                            members.append(name)
                except Exception:
                    pass
            
            return {
                "enum_class": enum_name,
                "values": sorted(members)
            }
        except Exception as exc:
            return {"status": "error", "error": f"Failed to get enum values: {exc}"}

    @mcp.tool()
    def set_pipe_ics(
        model_id: str,
        cc: int,
        pressure: float | list[float],
        temperature: float | list[float],
        void_fraction: float | list[float] = 0.0,
        ic_format: int | str = 3,
    ) -> dict:
        """Set initial conditions (pressure, temperature, void fraction, format) on a PIPE.

        Broadcasts scalars to all cells automatically.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.
        pressure : float or list[float]
            Pressure in Pa (scalar or list of size cell count).
        temperature : float or list[float]
            Temperature in K (scalar or list of size cell count).
        void_fraction : float or list[float], default 0.0
            Liquid/gas void fraction (scalar or list of size cell count).
        ic_format : int or str, default 3 (Press_Temp_Equilib_Cond)
            Format integer code or name:
            - 0 or "Press_Liq_E_Vap_E_Void_Frac"
            - 1 or "Temp_Qual"
            - 2 or "Pressure_Quality"
            - 3 or "Press_Temp_Equilib_Cond"
            - 4 or "Temp_Qual_NC_Qual"
            - 5 or "Press_Liq_E_Vap_E_Vap_Void_Frac_NC_Qual"
            - 6 or "Press_Temp_Qual"
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, cc)

        if comp is None:
            return {"status": "error", "error": f"Component CC {cc} not found in model"}
        if ctype != "PIPE":
            return {"status": "error", "error": f"Component CC {cc} is a {ctype}, not a PIPE"}

        try:
            _set_pipe_ics_impl(comp, pressure, temperature, void_fraction, ic_format)
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to set PIPE ICs: {exc}"}

    @mcp.tool()
    def set_pipe_geometry(
        model_id: str,
        cc: int,
        flow_area: float | list[float],
        length: float | list[float],
        hydraulic_diameter: float | list[float],
        vertical_angle: float | list[float] = 90.0,
        wall_roughness: float | list[float] = 4.6e-5,
    ) -> dict:
        """Set geometry (flow area, length, hydraulic diameter, angle, roughness) on a PIPE.

        Broadcasts scalars to all cells (and junctions between cells) automatically.

        Parameters
        ----------
        model_id : str
        cc : int
            Component number.
        flow_area : float or list[float]
            Flow area in m² (scalar or list of size cell count).
        length : float or list[float]
            Cell length in m (scalar or list of size cell count).
        hydraulic_diameter : float or list[float]
            Junction hydraulic diameter in m (scalar or list of size cell count or cell count - 1).
        vertical_angle : float or list[float], default 90.0
            Cell vertical angle in degrees (scalar or list of size cell count).
        wall_roughness : float or list[float], default 4.6e-5
            Cell wall roughness in m (scalar or list of size cell count).
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, cc)

        if comp is None:
            return {"status": "error", "error": f"Component CC {cc} not found in model"}
        if ctype != "PIPE":
            return {"status": "error", "error": f"Component CC {cc} is a {ctype}, not a PIPE"}

        try:
            _set_pipe_geom_impl(comp, flow_area, length, hydraulic_diameter, vertical_angle, wall_roughness)
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to set PIPE geometry: {exc}"}

    @mcp.tool()
    def get_component_schema(component_type: str) -> dict:
        """Return the documentation and key properties for a RELAP component type.

        Parameters
        ----------
        component_type : str
            One of: PIPE, SINGLE_VOLUME, TIME_DEPENDENT_VOLUME, SINGLE_JUNCTION,
            TIME_DEPENDENT_JUNCTION, VALVE, HEAT_STRUCTURE, CONTROL_BLOCK.
        """
        ct = component_type.upper()
        if ct not in COMPONENT_MAP:
            return {
                "error": f"Unknown component type '{component_type}'",
                "valid_types": list(COMPONENT_MAP.keys()),
            }

        schemas = {
            "PIPE": {
                "description": "Multi-cell 1-D hydraulic pipe component.",
                "initializer_fields": {
                    "cells": "int — number of volumes (cells), default 1. Can also use 'num_cells' or 'numberOfCells'."
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "flow_area": "float or list[float] — flow area in m²",
                    "x_length": "float or list[float] — volume length in m",
                    "hydraulic_diameter": "float or list[float] — hydraulic diameter in m",
                    "vertical_angle": "float or list[float] — vertical angle in degrees",
                    "x_wall_roughness": "float or list[float] — wall roughness in m (default 4.6e-5)",
                    "pressure": "float or list[float] — initial pressure in Pa",
                    "temperature": "float or list[float] — initial temperature in K",
                    "void_fraction": "float or list[float] — initial void fraction (0 for liquid, 1 for steam)",
                    "ic_input_format": "int or list[int] — initial condition format: 0=Press_Liq_E_Vap_E_Void_Frac, 3=Press_Temp_Equilib_Cond (default)"
                },
                "guidance": "Use set_pipe_geometry() and set_pipe_ics() for convenient bulk/uniform geometry and initial condition setting."
            },
            "SINGLE_VOLUME": {
                "description": "Single hydraulic volume component.",
                "initializer_fields": {},
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "flow_area": "float — flow area in m²",
                    "x_length": "float — volume length in m",
                    "vertical_angle": "float — vertical angle in degrees. Automatically calculates dzx (elevation change).",
                    "dzx": "float — elevation change in m (automatically computed from length and angle)",
                    "x_wall_roughness": "float — wall roughness in m (default 4.6e-5)",
                    "pressure": "float — initial pressure in Pa",
                    "temperature": "float — initial temperature in K",
                    "void_fraction": "float — initial void fraction (0 for liquid, 1 for steam)",
                    "ic_input_format": "enum (CellICFormatSelEditorv) — e.g. 'CellICFormatSelEditorv.Press_Temp_Equilib_Cond'"
                }
            },
            "TIME_DEPENDENT_VOLUME": {
                "description": "Boundary condition volume with time-dependent properties (pressure, temperature, etc.).",
                "initializer_fields": {},
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "tdv_data": "list[list] — time-dependent table data (e.g. rows of [time, pressure, temperature])",
                    "ic_input_format_tdv": "enum (TDVTFlagSel) — table format selector: 'TDVTFlagSel.P_MT' (default) or 'TDVTFlagSel.P_LE_VE_VF'"
                }
            },
            "SINGLE_JUNCTION": {
                "description": "Junction connecting two volumes.",
                "initializer_fields": {
                    "area": "float — flow area in m² (default 0.0). Can also use 'flow_area'.",
                    "inlet": "str — source connection string in 9-digit format or component name.",
                    "outlet": "str — target connection string in 9-digit format or component name."
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "flow_area": "float — junction flow area in m²",
                    "inlet": "str — source connection string",
                    "outlet": "str — target connection string"
                }
            },
            "TIME_DEPENDENT_JUNCTION": {
                "description": "Time-dependent junction (boundary flow).",
                "initializer_fields": {
                    "area": "float — flow area in m²",
                    "inlet": "str — source connection string",
                    "outlet": "str — target connection string"
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "tdj_data": "list[list] — time-dependent table data (e.g. rows of [time, mass_flow] or [time, velocity])"
                }
            },
            "VALVE": {
                "description": "Junction component with flow control/valve behaviour.",
                "initializer_fields": {
                    "area": "float — flow area in m²",
                    "inlet": "str — source connection string",
                    "outlet": "str — target connection string"
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "valve_type": "enum (ValveTypeSel) — e.g. 'ValveTypeSel.Servo_Valve' or 'ValveTypeSel.Trip_Valve'",
                    "valve_table": "list[list] — valve normalized area table vs stem position",
                    "init_position": "float — initial stem position (0.0 to 1.0)"
                }
            },
            "HEAT_STRUCTURE": {
                "description": "Heat structure modeling conduction and heat transfer to fluid volumes.",
                "initializer_fields": {
                    "geometry": "int — geometry number (default 1)",
                    "mesh_point_num": "int — number of mesh points (default 2)"
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "left_volume": "str — left boundary volume connection (e.g. '101010000')",
                    "right_volume": "str — right boundary volume connection (e.g. '102010000')",
                    "left_b_cond": "int — left boundary type",
                    "right_b_cond": "int — right boundary type"
                }
            },
            "CONTROL_BLOCK": {
                "description": "Control block for logical and mathematical control operations.",
                "initializer_fields": {
                    "cb_type": "str — type of control block (default 'sum')"
                },
                "key_properties": {
                    "name": "str — component name (max 8 characters)",
                    "gain": "float — multiplier gain",
                    "lim_low": "float — lower limit",
                    "lim_high": "float — upper limit"
                }
            }
        }

        return schemas.get(ct, {"description": f"RELAP component type {ct}"})
