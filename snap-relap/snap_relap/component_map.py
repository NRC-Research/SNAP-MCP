"""RELAP component mappings.

Maps RELAP component types to their SNAP Python creation and listing methods.
"""

COMPONENT_MAP = {
    "PIPE": {
        "create": "create_pipe",
        "list": "pipes",
    },
    "SINGLE_VOLUME": {
        "create": "create_single_volume",
        "list": "single_volumes",
    },
    "TIME_DEPENDENT_VOLUME": {
        "create": "create_time_dependent_volume",
        "list": "time_dependent_volumes",
    },
    "SINGLE_JUNCTION": {
        "create": "create_single_junction",
        "list": "single_junctions",
    },
    "TIME_DEPENDENT_JUNCTION": {
        "create": "create_time_dependent_junction",
        "list": "time_dependent_junctions",
    },
    "VALVE": {
        "create": "create_valve",
        "list": "valves",
    },
    "PUMP": {
        "create": "create_pump",
        "list": "pumps",
    },
    "ACCUMULATOR": {
        "create": "create_accumulator",
        "list": "accumulators",
    },
    "HEAT_STRUCTURE": {
        "create": "create_heatstruct",
        "list": "heatstructs",
    },
    "CONTROL_BLOCK": {
        "create": "create_control_block",
        "list": "control_blocks",
    },
    "MATERIAL": {
        "create": "create_material",
        "list": "materials",
    },
    "INTERACTIVE": {
        "create": "create_interactive",
        "list": "interactives",
    },
}


def _coerce_list(raw) -> list:
    """Coerce single java proxies or collections into standard Python list."""
    if raw is None:
        return []
    if hasattr(raw, "__iter__") and not hasattr(raw, "java_object"):
        return list(raw)
    return [raw]


def find_component(model, cc_num: int):
    """Scan all collections to locate a component by its CC number."""
    for ctype, cfg in COMPONENT_MAP.items():
        try:
            getter = getattr(model, cfg["list"])
            items = _coerce_list(getter())
            for item in items:
                # RELAP component IDs or numbers are fetched via getCCnumber() or number
                cc = -1
                for attr in ("getCCnumber", "number", "getComponentNumber"):
                    try:
                        v = getattr(item, attr)
                        cc = int(v() if callable(v) else v)
                        break
                    except Exception:
                        pass
                if cc == cc_num:
                    return ctype, item
        except Exception:
            pass
    return None, None


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

