"""Convert AI-provided values to the types the SNAP Python API expects.

Rules:
  "ClassName.MethodName"   →  enums.ClassName.MethodName()
  "ClassName.MethodName()" →  same (trailing parens stripped; both forms accepted)
  list / primitive         →  passed through unchanged
  bool strings             →  bool
"""
from __future__ import annotations

import snap_trace.snap_env  # noqa: F401

# Human-friendly aliases → internal SNAP Python API attribute names.
# These resolve before the setattr call so the AI can use either form.
PROPERTY_ALIASES: dict[str, str] = {
    # FILL / BREAK geometry
    "equivalent_length": "dxin",
    "reservoir_volume":  "volin",
    # FILL / BREAK boundary conditions
    "liquid_temperature": "tlin",
    "liquid_temp":        "tlin",
    "vapor_temperature":  "tvin",
    "vapor_temp":         "tvin",
    "void_fraction":      "alpin",
    "mass_flow_rate":     "flowin",
    # Wall properties (PIPE, VESSEL, PUMP)
    "wall_roughness": "epsw",
    "roughness":      "epsw",
    # FILL signal-variable inputs
    "liquid_flow_sv": "ifmlsv",
    "vapor_flow_sv":  "ifmvsv",
    "liquid_temp_sv": "iftlsv",
    "vapor_temp_sv":  "iftvsv",
    "void_sv":        "ifasv",
    "pressure_sv":    "ifpsv",
    "nc_pressure_sv": "ifpasv",
}


def resolve_enum(value: str):
    """Return the enum instance for "ClassName.Method", or None if not found."""
    if not isinstance(value, str) or "." not in value:
        return None
    import snap.codes.trace.enums as _enums
    cls_name, _, method_name = value.partition(".")
    method_name = method_name.rstrip("()")  # accept "VessType.RPV()" or "VessType.RPV"
    cls = getattr(_enums, cls_name, None)
    if cls is None:
        return None
    method = getattr(cls, method_name, None)
    if method is None:
        return None
    try:
        return method()
    except Exception:
        return None


def convert(value):
    """Convert a value from the AI representation to the SNAP API type."""
    if isinstance(value, str):
        # Enum check first
        enum_val = resolve_enum(value)
        if enum_val is not None:
            return enum_val
        # Boolean strings
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
    return value


def _suggest_property(comp, name: str) -> str:
    """Build a ' did you mean …; settable properties: …' hint for a bad name.

    String distance alone misses domain synonyms (e.g. a BREAK has no 'pout' —
    the field is 'pin' — and those aren't close strings), so the hint also lists
    the component's real settable properties. Returns '' if none can be read.
    Runs only on the error path, so the per-attribute getattr cost is fine.
    """
    import difflib
    # Internal/identity attributes that are reachable but not physics inputs.
    _internal = {"java_object", "model", "table", "compid", "cc_number", "number"}
    props: list[str] = []
    try:
        for a in dir(comp):
            if a.startswith("_") or a.endswith(("_enabled", "_table")) or a in _internal:
                continue
            try:
                v = getattr(comp, a)
            except Exception:
                continue
            if callable(v) and not hasattr(v, "__self__"):
                continue  # unbound Java/Python method, not a settable property
            props.append(a)
    except Exception:
        return ""
    if not props:
        return ""
    props.sort()
    parts = []
    close = difflib.get_close_matches(name, props, n=3, cutoff=0.6)
    if close:
        parts.append("did you mean " + ", ".join(repr(c) for c in close) + "?")
    shown = ", ".join(props[:30])
    if len(props) > 30:
        shown += f", … (+{len(props) - 30} more)"
    parts.append("settable properties: " + shown)
    return " " + " ".join(parts)


def set_property(comp, name: str, value) -> None:
    """Set an attribute on a SNAP component, converting the value first.

    For table/array properties the value should be a list; for table rows
    (initial conditions) it should be a list of lists that will be read
    row by row via .read().
    """
    # Apply human-friendly alias before doing anything else.
    name = PROPERTY_ALIASES.get(name, name)

    converted = convert(value)

    # Table of lists → write via the table's own .read() if available,
    # then fall back to row-by-row __setitem__, then to row.read().
    if isinstance(converted, list) and converted and isinstance(converted[0], list):
        table = getattr(comp, name)
        rows = [[convert(v) for v in row] for row in converted]
        if hasattr(table, "read") and callable(table.read):
            table.read(rows)
        else:
            for i, row in enumerate(rows):
                try:
                    table[i] = row
                except Exception:
                    table[i].read(row)
        return

    # Simple list → set directly (SNAP handles assignment for array properties)
    if isinstance(converted, list):
        converted = [convert(v) for v in converted]

    # Pre-flight: verify the attribute is reachable on this object.
    # When SNAP's __getattr__ raises AttributeError for an unknown Java property
    # the setattr would silently create a Python-only instance attribute that
    # never reaches the SNAP data model.  Surfacing the error here lets the
    # caller catch it instead of getting a silent no-op.
    try:
        existing = getattr(comp, name)
    except AttributeError as exc:
        # Unknown property — enrich with close matches + the real settable
        # property names so the caller (and the model) learns the right one.
        raise AttributeError(f"{exc}.{_suggest_property(comp, name)}") from None
    except Exception:
        # Py4JError or similar — attribute may still be settable; let setattr try.
        existing = None
    else:
        if callable(existing) and not hasattr(existing, "__self__"):
            raise AttributeError(
                f"'{name}' is a method, not a settable property"
            )

    setattr(comp, name, converted)
