"""Maps MCP component type strings to SNAP TraceModel factory/accessor methods.

Each entry documents:
  create        str   — TraceModel method name for creation
  list          str   — TraceModel method name returning all instances (or None)
  initializer   str   — component_initializer() category, or None
  first_arg     str   — if set, the property name in `properties` dict that
                        becomes the first positional arg to the create method
                        (e.g. ControlTypeSel for CONTROL_BLOCK)
"""
from __future__ import annotations

COMPONENT_MAP: dict[str, dict] = {
    "PIPE": {
        "create": "create_pipe",
        "list": "pipes",
        "initializer": "Pipes",
        "first_arg": None,
    },
    "FILL": {
        "create": "create_fill",
        "list": "fills",
        "initializer": None,
        "first_arg": None,
    },
    "BREAK": {
        "create": "create_break",
        "list": "breaks",
        "initializer": None,
        "first_arg": None,
    },
    "PUMP": {
        "create": "create_pump",
        "list": "pumps",
        "initializer": "Pumps",
        "first_arg": None,
    },
    "VALVE": {
        "create": "create_valve",
        "list": "valves",
        "initializer": "Valves",
        "first_arg": None,
    },
    "VESSEL": {
        "create": "create_vessel",
        "list": "vessels",
        "initializer": "Vessels",
        "first_arg": None,
    },
    "PLENUM": {
        "create": "create_plenum",
        "list": "plenums",
        "initializer": None,
        "first_arg": None,
    },
    "TEE": {
        "create": "create_tee",
        "list": "tees",
        "initializer": None,
        "first_arg": None,
    },
    "SEPARATOR": {
        "create": "create_separator",
        "list": "separators",
        "initializer": "Separators",
        "first_arg": None,
    },
    "TURBINE": {
        "create": "create_turbine",
        "list": "turbines",
        "initializer": None,
        "first_arg": None,
    },
    "HEATER": {
        "create": "create_heater",
        "list": "heaters",
        "initializer": "Heaters",
        "first_arg": None,
    },
    "HEAT_STRUCTURE": {
        "create": "create_heatstructure",
        "list": "heatstructures",
        "initializer": "Heat Structures",
        "first_arg": None,
    },
    "POWER": {
        "create": "create_power",
        "list": "powers",
        "initializer": None,
        "first_arg": None,
    },
    "CONTROL_BLOCK": {
        "create": "create_control_block",
        "list": "control_blocks",
        "initializer": None,
        # supply as: properties["control_type"] = "ControlTypeSel.Interactive_Variable"
        "first_arg": "control_type",
    },
    "SIGNAL_VARIABLE": {
        "create": "create_signal_variable",
        "list": "signal_variables",
        "initializer": None,
        # supply as: properties["signal_type"] = "SignalTypeSel.Liquid_Temperature"
        "first_arg": "signal_type",
    },
    "SIGNAL_EXPRESSION": {
        "create": "create_signal_expression",
        "list": None,
        "initializer": None,
        "first_arg": None,
    },
    "TRIP": {
        "create": "create_trip",
        "list": "trips",
        "initializer": None,
        "first_arg": None,
    },
    "TRIP_CONTROLLER": {
        "create": "create_trip_controller",
        "list": None,
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_COMPARTMENT": {
        "create": "create_contan_compartment",
        "list": "contan_compartments",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_HEAT_STRUCTURE": {
        "create": "create_contan_heatstructure",
        "list": "contan_heatstructures",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_COOLER": {
        "create": "create_contan_cooler",
        "list": "contan_coolers",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_FAN_COOLER": {
        "create": "create_contan_fan_cooler",
        "list": "contan_fan_coolers",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_PASSIVE_JUNCTION": {
        "create": "create_contan_passive_junction",
        "list": "contan_passive_junctions",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_FORCED_JUNCTION": {
        "create": "create_contan_forced_junction",
        "list": "contan_forced_junctions",
        "initializer": None,
        "first_arg": None,
    },
    "CONTAN_SINK_JUNCTION": {
        "create": "create_contan_sink_junction",
        "list": "contan_sink_junctions",
        "initializer": None,
        "first_arg": None,
    },
}

ALL_TYPES = sorted(COMPONENT_MAP.keys())


def _is_enum_string(value) -> bool:
    """Return True if the value looks like an enum string ("Class.Method")."""
    if not isinstance(value, str):
        return False
    if "." not in value:
        return False
    cls_name = value.split(".")[0]
    try:
        import snap.codes.trace.enums as _e
        return hasattr(_e, cls_name)
    except Exception:
        return False


def _coerce_list(val):
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def create_component(model, comp_type: str, comp_num: int,
                     properties: dict, initializer_props: dict | None):
    """Create a component and apply properties. Returns the component object."""
    from snap_trace.type_converter import convert, set_property

    cfg = COMPONENT_MAP.get(comp_type.upper())
    if cfg is None:
        raise ValueError(
            f"Unknown component type '{comp_type}'. "
            f"Valid types: {', '.join(ALL_TYPES)}"
        )

    create_fn = getattr(model, cfg["create"])
    props = dict(properties or {})

    # VESSEL exposes no 'name' setter — its label lives in 'ctitle'.  Remap so
    # callers can pass a uniform 'name' for every component type without
    # tripping the "property 'name' has no setter" warning.
    if comp_type.upper() == "VESSEL" and "name" in props and "ctitle" not in props:
        props["ctitle"] = props.pop("name")

    # --- build positional first arg if required (control_type / signal_type) ---
    first_arg_val = None
    if cfg["first_arg"]:
        raw = props.pop(cfg["first_arg"], None)
        if raw is None:
            raise ValueError(
                f"{comp_type} requires '{cfg['first_arg']}' in properties, "
                f"e.g. \"ControlTypeSel.Interactive_Variable\""
            )
        first_arg_val = convert(raw)

    # --- build and populate initializer if the component supports one ---
    initializer = None
    if cfg["initializer"] and initializer_props:
        initializer = model.component_initializer(cfg["initializer"])
        for k, v in initializer_props.items():
            set_property(initializer, k, v)

    # --- call the factory method ---
    if first_arg_val is not None:
        comp = create_fn(first_arg_val, comp_num)
    elif initializer is not None:
        comp = create_fn(initializer, comp_num)
    else:
        comp = create_fn(comp_num)

    # --- apply remaining properties ---
    # Set enum-valued properties first because they often gate other properties
    # (e.g. FILL.ifty must be set before FILL.flowin).
    enum_props = {k: v for k, v in props.items() if _is_enum_string(v)}
    scalar_props = {k: v for k, v in props.items() if not _is_enum_string(v)}

    failed: list[str] = []
    for k, v in {**enum_props, **scalar_props}.items():
        try:
            set_property(comp, k, v)
        except Exception as exc:
            failed.append(f"{k}={v!r}: {exc}")

    comp._snap_mcp_failed_props = failed  # stash for caller to report
    return comp


def find_component(model, comp_num: int):
    """Search every category and return the first component with this CC number.

    Returns (comp_type_str, component) or raises ValueError.
    """
    for comp_type, cfg in COMPONENT_MAP.items():
        list_method = cfg.get("list")
        if not list_method:
            continue
        try:
            comps = _coerce_list(getattr(model, list_method)())
            for comp in comps:
                try:
                    if int(comp.java_object.getCCnumber()) == comp_num:
                        return comp_type, comp
                except Exception:
                    pass
        except Exception:
            pass
    raise ValueError(f"No component with number {comp_num} found in model.")


def iter_all_components(model) -> list[tuple[str, object]]:
    """Yield (comp_type, component) for every component in the model."""
    results = []
    for comp_type, cfg in COMPONENT_MAP.items():
        list_method = cfg.get("list")
        if not list_method:
            continue
        try:
            comps = _coerce_list(getattr(model, list_method)())
            for comp in comps:
                results.append((comp_type, comp))
        except Exception:
            pass
    return results
