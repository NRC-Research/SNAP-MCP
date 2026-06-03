"""Component inspection and modification tools.

MELCOR package → Java category short-name fragment mapping:
    CVH  - Control Volume Hydrodynamics  (category contains "CVH")
    FL   - Flow Paths                    (category contains "FL")
    HS   - Heat Structures               (category contains "HS")
    COR  - Core                          (category contains "COR")
    BUR  - Burn package                  (category contains "BUR")
    DCH  - Direct Containment Heating    (category contains "DCH")
    RN   - Radionuclide transport        (category contains "RN")
    ESF  - Engineered Safety Features    (category contains "ESF")
    SP   - Spray systems                 (category contains "SP")
    CF   - Control Functions             (category contains "CF")

Category short names returned by the SNAP API include the full display name,
e.g. "Control Volumes (CVH)". Match by checking if the package code appears
inside the string rather than exact equality.

Setter dispatch strategy (MELCOR unit objects are not directly constructable
from Python, so Py4J cannot auto-coerce a Python float):

  1. CReal subclasses (Pressa, Temp, Length, Area, Volume, Velocity, …):
     Use the getter to obtain the existing CReal object, call setValue(double)
     on it to mutate it in-place, then pass it back to the setter.

  2. LengthControlArc (used by diamf, diamr, zfm, zto, …):
     getArc() → arc.getLength() → length_obj.setValue(double)
     → arc.setLength(length_obj).  No pass-back needed; arc is already linked.

  3. Integer CV references (kcvfm, kcvto, ibvl, ibvr, …):
     If the caller passes a string, look up the component by name in the model
     and extract its CC number.  Pass the integer to the setter.

  4. Primitive / String setters: direct call as before.
"""

from __future__ import annotations

from snap_melcor import session as _session

try:
    import snap_melcor.bindings.components as _comps
    _BINDINGS_AVAILABLE = True
except ImportError:
    _comps = None
    _BINDINGS_AVAILABLE = False


_KNOWN_PACKAGES = ["CVH", "FL", "HS", "COR", "BUR", "DCH", "RN", "ESF", "SP", "CF"]

# Human-friendly aliases → actual Java setter names (without "set" prefix).
# Keys are lowercase; values are camelCase as the Java API expects.
# Confirmed against MELCOR2X 2.7.1 live API investigation.
_PROPERTY_ALIASES: dict[str, str] = {
    # CVH (VolumeComponent) — initial conditions
    "volume":           "pvolr",       # pool volume, right state (m³)
    "pool_volume":      "pvolr",
    "pressure":         "pncg",        # total NCG pressure (Pa)
    "temperature":      "tatmr",       # atmosphere temperature, right state (K)
    "atm_temp":         "tatmr",
    "pool_temp":        "tpolr",       # pool liquid temperature, right state (K)
    "pool_elevation":   "zpolr",       # pool surface elevation (m)
    "cv_type":          "icvtyp",      # control volume type flag
    # FL (FlowPath) — geometry and connections
    "from_cv":          "kcvfm",       # from-CV reference (CV name → int CC#)
    "to_cv":            "kcvto",       # to-CV reference (CV name → int CC#)
    "flow_area":        "flara",       # flow path cross-sectional area (m²)
    "diameter":         "diamf",       # hydraulic diameter forward (m) — LengthControlArc
    "diameter_forward": "diamf",
    "diameter_reverse": "diamr",       # hydraulic diameter reverse (m)
    "length":           "fllen",       # flow path length (m)
    "elevation_from":   "zfm",         # from-junction center elevation (m)
    "elevation_to":     "zto",         # to-junction center elevation (m)
    # HS (HeatComponent) — geometry and boundary conditions
    "geometry":         "igeom",       # 1=planar slab, 2=cylinder, 3=sphere
    "initial_temp":     "initialTemp", # initial temperature (K)
    "left_bc":          "ibcl",        # left-side boundary condition type
    "right_bc":         "ibcr",        # right-side boundary condition type
    "left_htc":         "xhtfcl",      # left convective heat transfer coefficient
    "right_htc":        "xhtfcr",      # right convective heat transfer coefficient
    "left_cv":          "ibvl",        # left-side connected CV reference (int CC#)
    "right_cv":         "ibvr",        # right-side connected CV reference (int CC#)
    "left_surface_area":  "asurfl",    # left surface area (m²)
    "right_surface_area": "asurfr",    # right surface area (m²)
}

# Setter stems whose parameter is an integer CV/component number.
# If the caller passes a string, we resolve it to the CC number.
_CV_REF_SETTERS: frozenset[str] = frozenset(
    ["kcvfm", "kcvto", "ibvl", "ibvr"]
)


def _resolve_property(prop: str) -> str:
    """Map a human-friendly property name to the canonical Java setter stem."""
    return _PROPERTY_ALIASES.get(prop.lower(), prop)


def _call_setter(java_comp, stem: str, value, java_model=None) -> None:
    """Dispatch a property set through the correct Java calling convention.

    Tries each pattern in order without Java reflection probing (getParameters()
    hangs under Java module-opens restrictions).  Four patterns:

    1. CV reference  — resolve name → int CC# for kcvfm/kcvto/ibvl/ibvr
    2. Direct call   — primitives (int, float, String)
    3. LengthControlArc — diamf/diamr/zfm/zto; getter() → getLength().setValue()
    4. CReal subclass  — Pressa/Temp/Length/Area/…; getter().setValue() → setter()

    Parameters
    ----------
    java_comp : Py4J JavaObject
    stem : str   — setter stem without "set", e.g. "pvolr", "diamf"
    value : scalar
    java_model : Py4J JavaObject, optional  — needed for CV-ref name resolution
    """
    setter_name = "set%s%s" % (stem[0].upper(), stem[1:])
    getter_name = "get%s%s" % (stem[0].upper(), stem[1:])

    # 1. CV reference setters: resolve string name → integer CC#
    if stem.lower() in _CV_REF_SETTERS and isinstance(value, str):
        target = _find_component(java_model, value) if java_model else None
        if target is None:
            raise ValueError(
                "Component '%s' not found in model (needed for %s)" % (value, setter_name)
            )
        value = int(target.getCCnumber())
        getattr(java_comp, setter_name)(value)
        return

    # 2. Direct call (primitives, String, already-correct Java objects)
    try:
        getattr(java_comp, setter_name)(value)
        return
    except Exception as direct_exc:
        direct_exc_str = str(direct_exc)

    # 3. LengthControlArc pattern (diamf, diamr, zfm, zto, …)
    #    Detect by trying getLength() on the object returned by the getter.
    if hasattr(java_comp, getter_name):
        try:
            arc = getattr(java_comp, getter_name)()
            length_obj = arc.getLength()          # raises if not a LengthControlArc
            length_obj.setValue(float(value))
            arc.setLength(length_obj)
            return
        except Exception:
            pass  # not a LengthControlArc — fall through to CReal

        # 4. CReal get-mutate-set (Pressa, Temp, Length, Area, Volume, …)
        try:
            creal_obj = getattr(java_comp, getter_name)()
            creal_obj.setValue(float(value))      # raises if not a CReal
            getattr(java_comp, setter_name)(creal_obj)
            return
        except Exception as creal_exc:
            raise Exception(
                "Direct call failed (%s); LengthControlArc and CReal patterns "
                "also failed: %s" % (direct_exc_str, creal_exc)
            )

    raise Exception(direct_exc_str)


def _find_category(java_model, pkg_code: str):
    """Return the first Java category whose short name contains pkg_code, or None."""
    pkg_upper = pkg_code.upper()
    for cat in java_model.getCategories():
        try:
            short = str(cat.getShortName()).upper()
            if pkg_upper in short:
                return cat
        except Exception:
            pass
    return None


def _find_component(java_model, name: str):
    """Search all categories for a component with the given name, return Java object or None."""
    for cat in java_model.getCategories():
        try:
            comp = java_model.findComponentByName(name, cat)
            if comp is not None:
                return comp
        except Exception:
            pass
    # Fall back to iterating the flat component list
    try:
        for comp in java_model.getComponents():
            try:
                if str(comp.getName()) == name:
                    return comp
            except Exception:
                pass
    except Exception:
        pass
    return None


def _comp_package(comp, java_model) -> str:
    """Best-effort determination of which package owns a component."""
    for pkg in _KNOWN_PACKAGES:
        cat = _find_category(java_model, pkg)
        if cat is None:
            continue
        try:
            found = java_model.findComponentByName(str(comp.getName()), cat)
            if found is not None:
                return pkg
        except Exception:
            pass
    return "?"


def _full_schema(cls) -> dict:
    """Return merged schema dict from cls and all parent classes (via MRO)."""
    schema = {}
    for c in reversed(cls.__mro__):
        schema.update(getattr(c, '_SCHEMA', {}))
    return schema


def _java_simple_name(java_obj) -> str:
    """Return the Java simple class name for a Py4J-proxied object.

    type(java_obj).__name__ always returns 'JavaObject' in Py4J. Use the
    Java reflection API instead to get the actual class name.
    """
    try:
        return str(java_obj.getClass().getSimpleName())
    except Exception:
        return type(java_obj).__name__


def _find_component_class(java_obj):
    """Return the binding class for a Py4J Java object, or None."""
    return _find_binding_by_name(_java_simple_name(java_obj))


def _find_binding_by_name(name: str):
    """Return the binding class for a Java simple class name string, or None."""
    if not _BINDINGS_AVAILABLE:
        return None
    cls = getattr(_comps, name, None)
    if cls is not None:
        return cls
    for variant in (name + "Component", name.replace("Component", ""),
                    name + "Bean", "Abstract" + name):
        cls = getattr(_comps, variant, None)
        if cls is not None:
            return cls
    return None


def register_component_tools(mcp) -> None:

    @mcp.tool()
    def list_components(model_id: str, package: str | None = None) -> list[dict]:
        """List all components in the model, optionally filtered by package.

        Parameters
        ----------
        model_id : str
        package : str, optional
            MELCOR package code (CVH, FL, HS, COR, BUR, DCH, RN, ESF, SP, CF).
            If None, returns all components across all packages.

        Returns
        -------
        list of dicts with keys: name, number, type, package
        """
        model = _session.get(model_id)
        jm = model.java_model

        results = []
        if package:
            # Enumerate only the requested package's category
            cat = _find_category(jm, package.upper())
            if cat is None:
                return [{"error": f"Package '{package}' not found in model"}]
            for comp in jm.getComponents():
                try:
                    found = jm.findComponentByName(str(comp.getName()), cat)
                    if found is not None:
                        results.append({
                            "name": str(comp.getName()),
                            "number": int(comp.getCCnumber()),
                            "type": _java_simple_name(comp),
                            "package": package.upper(),
                        })
                except Exception:
                    pass
        else:
            # Flat enumeration of all components
            try:
                for comp in jm.getComponents():
                    try:
                        results.append({
                            "name": str(comp.getName()),
                            "number": int(comp.getCCnumber()),
                            "type": _java_simple_name(comp),
                        })
                    except Exception:
                        results.append({"error": "metadata unavailable"})
            except Exception as exc:
                return [{"error": str(exc)}]

        return results

    @mcp.tool()
    def get_component(model_id: str, name: str) -> dict:
        """Return all accessible properties of a named MELCOR component.

        Parameters
        ----------
        model_id : str
        name : str
            Component name as it appears in list_components (e.g. "CV-DOME").

        Returns
        -------
        dict with property name → value for each readable property,
        or an 'error' key if the component is not found.
        """
        model = _session.get(model_id)
        jm = model.java_model

        java_comp = _find_component(jm, name)
        if java_comp is None:
            return {"error": f"Component {name!r} not found"}

        comp_type_name = _java_simple_name(java_comp)
        comp_cls = _find_component_class(java_comp)

        if comp_cls is None:
            # No generated binding — walk Java getters for a best-effort property dump
            props = {}
            for m in java_comp.getClass().getMethods():
                mname = str(m.getName())
                if not mname.startswith("get") or mname in ("getClass",):
                    continue
                if m.getParameterCount() != 0:
                    continue
                prop_key = mname[3].lower() + mname[4:]
                try:
                    val = getattr(java_comp, mname)()
                    props[prop_key] = str(val)
                except Exception:
                    pass
            return {"name": name, "type": comp_type_name,
                    "note": "No Python binding; Java getter values shown",
                    "properties": props}

        schema = _full_schema(comp_cls)
        wrapper = comp_cls(model, java_comp)
        result = {"name": name, "type": comp_type_name, "properties": {}}
        for prop_name in schema:
            try:
                val = getattr(wrapper, prop_name)
                if hasattr(val, "value"):
                    val = val.value
                result["properties"][prop_name] = val
            except Exception:
                pass
        return result

    @mcp.tool()
    def get_component_schema(component_type: str) -> dict:
        """Describe the settable properties for a given MELCOR component type.

        Parameters
        ----------
        component_type : str
            MELCOR component Java class name (e.g. "FlowPath", "ControlVolume").
            Call list_components to see the 'type' field for existing components.

        Returns
        -------
        dict with keys:
            component_type (str): the class name looked up
            properties (dict): {prop_name → {display, type, description}}
        """
        comp_cls = _find_binding_by_name(component_type)
        if comp_cls is None:
            available = sorted(
                n for n in dir(_comps) if not n.startswith("_")
                and isinstance(getattr(_comps, n, None), type)
            ) if _BINDINGS_AVAILABLE else []
            return {
                "error": f"Unknown component type: {component_type!r}",
                "available_types": available[:50],
            }
        return {
            "component_type": component_type,
            "properties": _full_schema(comp_cls),
        }

    @mcp.tool()
    def add_component(
        model_id: str,
        package: str,
        name: str,
        properties: dict | None = None,
    ) -> dict:
        """Add a new component to the model.

        Parameters
        ----------
        model_id : str
        package : str
            MELCOR package code: CVH, FL, HS, COR, BUR, DCH, RN, ESF, SP, CF.
        name : str
            Name for the new component (e.g. "CV-DOME", "FL-001").
        properties : dict, optional
            Initial property values to set after creation.
            Keys are either human-friendly aliases (see below) or the camelCase
            Java setter name without the "set" prefix. Human-friendly aliases:
              CVH: "volume" (m³), "pressure" (Pa), "temperature" (K atm),
                   "pool_temp" (K), "pool_elevation" (m)
              FL:  "from_cv" (CV name), "to_cv" (CV name), "flow_area" (m²),
                   "diameter" (m), "length" (m), "elevation_from" (m), "elevation_to" (m)
              HS:  "geometry" (1=slab,2=cyl,3=sphere), "initial_temp" (K),
                   "left_bc" / "right_bc", "left_htc" / "right_htc" (W/m²K),
                   "left_surface_area" / "right_surface_area" (m²)
            Example: {"volume": 100.0, "pressure": 1.013e5, "temperature": 300.0}

        Returns
        -------
        dict with keys: status, name, number, type, package, warnings
        """
        model = _session.get(model_id)
        jm = model.java_model

        cat = _find_category(jm, package.upper())
        if cat is None:
            return {"status": "error",
                    "error": f"Package '{package}' not found in model categories"}

        try:
            comp = cat.createComponent(jm)
            comp.addToModel(jm)
        except Exception as exc:
            return {"status": "error", "error": f"createComponent failed: {exc}"}

        try:
            comp.setName(name)
        except Exception as exc:
            return {"status": "error", "error": f"setName failed: {exc}"}

        warnings = []
        if properties:
            for prop, val in properties.items():
                resolved = _resolve_property(prop)
                try:
                    _call_setter(comp, resolved, val, java_model=jm)
                except Exception as exc:
                    warnings.append("%r: %s" % (prop, exc))

        result = {
            "status": "ok",
            "package": package.upper(),
            "name": name,
        }
        try:
            result["number"] = int(comp.getCCnumber())
        except Exception:
            pass
        try:
            result["type"] = _java_simple_name(comp)
        except Exception:
            pass
        if warnings:
            result["warnings"] = warnings
        return result

    @mcp.tool()
    def set_component_property(
        model_id: str,
        component_name: str,
        property_name: str,
        value: str | int | float,
    ) -> dict:
        """Set a property on a MELCOR component.

        Parameters
        ----------
        model_id : str
        component_name : str
            Component name as shown by list_components.
        property_name : str
            Human-friendly alias (e.g. "volume", "pressure", "from_cv") or
            the camelCase Java setter name without "set" prefix (e.g. "pvolr",
            "kcvfm", "initialTemp"). The same aliases supported by add_component
            are recognized here.
        value : str | int | float
            New value. For CV references (from_cv, to_cv) pass the CV name string.

        Returns
        -------
        dict with keys: status, component_name, property_name, resolved_setter, new_value
        """
        model = _session.get(model_id)
        jm = model.java_model

        java_comp = _find_component(jm, component_name)
        if java_comp is None:
            return {"status": "error",
                    "error": f"Component {component_name!r} not found"}

        resolved = _resolve_property(property_name)
        try:
            _call_setter(java_comp, resolved, value, java_model=jm)
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

        return {
            "status": "ok",
            "component_name": component_name,
            "property_name": property_name,
            "resolved_setter": setter_name,
            "new_value": value,
        }

    @mcp.tool()
    def list_component_properties(model_id: str, component_name: str) -> dict:
        """List all settable properties for a MELCOR component via Java reflection.

        Returns the Java simple class name and all setter method names (without
        the "set" prefix) so you can pass them to set_component_property or as
        property keys in add_component.

        Parameters
        ----------
        model_id : str
        component_name : str
            Component name as shown by list_components.

        Returns
        -------
        dict with keys: name, java_type, setters (list[str]), aliases (dict)
        """
        model = _session.get(model_id)
        jm = model.java_model

        java_comp = _find_component(jm, component_name)
        if java_comp is None:
            return {"error": f"Component {component_name!r} not found"}

        java_type = _java_simple_name(java_comp)
        setters = sorted(
            str(m.getName())[3:]          # strip leading "set"
            for m in java_comp.getClass().getMethods()
            if str(m.getName()).startswith("set")
            and m.getParameterCount() == 1
        )

        # Show which human-friendly aliases map to setters on this component
        aliases = {
            alias: canonical
            for alias, canonical in _PROPERTY_ALIASES.items()
            if f"set{canonical[0].upper()}{canonical[1:]}" in
               {f"set{s[0].upper()}{s[1:]}" if s else "" for s in setters}
               or canonical in [s[0].lower() + s[1:] for s in setters]
        }

        return {
            "name": component_name,
            "java_type": java_type,
            "setters": setters,
            "aliases": aliases,
        }
