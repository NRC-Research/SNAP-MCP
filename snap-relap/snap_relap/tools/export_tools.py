"""Validation and export tools."""

from __future__ import annotations
import tempfile
import os
import math

from snap_relap import session as _session
from snap_relap.component_map import COMPONENT_MAP, _coerce_list, find_component, iter_all_components



def _get_cc(comp) -> int:
    """Helper to find the CC number of a component."""
    cc = -1
    for attr in ("getCCnumber", "number", "getComponentNumber"):
        try:
            v = getattr(comp, attr)
            cc = int(v() if callable(v) else v)
            break
        except Exception:
            pass
    return cc


def _get_cell_flow_area(model, cc: int, cell_idx: int) -> float:
    """Helper to resolve a volume cell's flow area."""
    ctype, comp = find_component(model, cc)
    if comp is None:
        return 0.0
    try:
        if ctype == "PIPE":
            idx = cell_idx - 1
            if 0 <= idx < len(comp.x_area):
                return float(comp.x_area[idx])
        else:
            return float(getattr(comp, "flow_area", 0.0))
    except Exception:
        pass
    return 0.0


def _python_model_check(model) -> tuple[list[str], list[str]]:
    """Perform Python-level validation checks.

    Includes checks for unconnected junctions, heat structures, unknown thermodynamic properties,
    zero hydraulic diameters, missing/empty time tables, and 10:1 flow area mismatches.
    """
    errors = []
    warnings = []

    def is_invalid_val(val) -> bool:
        if val is None:
            return True
        val_str = str(val).strip()
        if val_str.lower() in ("unknown", "nan", "", "disabled"):
            return True
        if "disabled" in val_str.lower() or "ValueDisabledException" in val_str:
            return True
        return False

    def is_invalid_num(val) -> bool:
        try:
            val_f = float(val)
            if math.isnan(val_f):
                return True
            return False
        except (TypeError, ValueError):
            return is_invalid_val(val)

    # 1. Check volume/cell thermodynamics and geometry (PIPE, SINGLE_VOLUME, TIME_DEPENDENT_VOLUME)
    try:
        # A. PIPEs
        if hasattr(model, "pipes"):
            for comp in _coerce_list(model.pipes()):
                cc = _get_cc(comp)
                # Pressure
                try:
                    for i, p_val in enumerate(comp.pressure):
                        if is_invalid_num(p_val):
                            errors.append(f"PIPE {cc} cell {i+1}: pressure is invalid or unknown")
                except Exception:
                    pass
                # Temperature
                try:
                    for i, t_val in enumerate(comp.temperature):
                        if is_invalid_num(t_val):
                            errors.append(f"PIPE {cc} cell {i+1}: temperature is invalid or unknown")
                except Exception:
                    pass
                # x_area
                try:
                    for i, a_val in enumerate(comp.x_area):
                        if is_invalid_num(a_val) or float(a_val) <= 0.0:
                            errors.append(f"PIPE {cc} cell {i+1}: flow area is invalid, unknown, or zero")
                except Exception:
                    pass
                # x_length
                try:
                    for i, l_val in enumerate(comp.x_length):
                        if is_invalid_num(l_val) or float(l_val) <= 0.0:
                            errors.append(f"PIPE {cc} cell {i+1}: length is invalid, unknown, or zero")
                except Exception:
                    pass
                # Junction hydraulic_diameter (size N-1)
                try:
                    for i, hd_val in enumerate(comp.hydraulic_diameter):
                        if is_invalid_num(hd_val) or float(hd_val) <= 0.0:
                            errors.append(f"PIPE {cc} junction {i+1}: hydraulic diameter is invalid, unknown, or zero")
                except Exception:
                    pass
    except Exception:
        pass

    try:
        # B. SINGLE_VOLUMEs
        if hasattr(model, "single_volumes"):
            for comp in _coerce_list(model.single_volumes()):
                cc = _get_cc(comp)
                for prop, desc in [("pressure", "pressure"), ("temperature", "temperature"), ("flow_area", "flow area"), ("x_length", "length")]:
                    try:
                        val = getattr(comp, prop)
                        if is_invalid_num(val):
                            errors.append(f"SINGLE_VOLUME {cc}: {desc} is invalid or unknown")
                        elif prop in ("flow_area", "x_length") and float(val) <= 0.0:
                            errors.append(f"SINGLE_VOLUME {cc}: {desc} must be greater than zero")
                    except Exception:
                        pass
    except Exception:
        pass

    try:
        # C. TIME_DEPENDENT_VOLUMEs
        if hasattr(model, "time_dependent_volumes"):
            for comp in _coerce_list(model.time_dependent_volumes()):
                cc = _get_cc(comp)
                try:
                    table = getattr(comp, "tdv_data", None)
                    if table is None or len(table) == 0:
                        errors.append(f"TIME_DEPENDENT_VOLUME {cc}: tdv_data table is empty or missing")
                except Exception:
                    pass
    except Exception:
        pass

    # 2. Check junctions (SINGLE_JUNCTION, TIME_DEPENDENT_JUNCTION, VALVE, PUMP)
    junction_getters = [
        ("single_junctions", "Single Junction"),
        ("time_dependent_junctions", "Time Dependent Junction"),
        ("valves", "Valve"),
        ("pumps", "Pump"),
    ]
    
    for getter, label in junction_getters:
        try:
            fn = getattr(model, getter, None)
            if fn is not None:
                comps = _coerce_list(fn())
                for comp in comps:
                    cc = _get_cc(comp)
                    
                    # Connection checks
                    inlet_unconnected = False
                    outlet_unconnected = False
                    
                    # Check inlet
                    try:
                        inlet = getattr(comp, "inlet", None)
                        if inlet is None or str(inlet).strip() in ("", "0", "0000000"):
                            errors.append(f"{label} {cc}: inlet is unconnected")
                            inlet_unconnected = True
                    except Exception:
                        pass
                        
                    # Check outlet
                    try:
                        outlet = getattr(comp, "outlet", None)
                        if outlet is None or str(outlet).strip() in ("", "0", "0000000"):
                            errors.append(f"{label} {cc}: outlet is unconnected")
                            outlet_unconnected = True
                    except Exception:
                        pass

                    # Zero hydraulic diameter on junction
                    try:
                        hd = float(getattr(comp, "hydraulic_diameter", 0.0))
                        if hd <= 0.0:
                            errors.append(f"{label} {cc}: hydraulic diameter is zero or invalid")
                    except Exception:
                        pass

                    # Check mismatched flow areas if connected
                    try:
                        j_area = float(getattr(comp, "flow_area", 0.0))
                        if j_area > 0.0:
                            if not inlet_unconnected:
                                inlet_str = str(getattr(comp, "inlet", ""))
                                if len(inlet_str) >= 3:
                                    from_cc = int(inlet_str[:3])
                                    from_cell = int(inlet_str[3:5])
                                    from_area = _get_cell_flow_area(model, from_cc, from_cell)
                                    if from_area > 0.0:
                                        ratio = max(j_area / from_area, from_area / j_area)
                                        if ratio > 10.0:
                                            warnings.append(
                                                f"{label} {cc}: area ratio with inlet volume {from_cc} cell {from_cell} exceeds 10:1 (ratio={ratio:.1f})"
                                            )
                            
                            if not outlet_unconnected:
                                outlet_str = str(getattr(comp, "outlet", ""))
                                if len(outlet_str) >= 3:
                                    to_cc = int(outlet_str[:3])
                                    to_cell = int(outlet_str[3:5])
                                    to_area = _get_cell_flow_area(model, to_cc, to_cell)
                                    if to_area > 0.0:
                                        ratio = max(j_area / to_area, to_area / j_area)
                                        if ratio > 10.0:
                                            warnings.append(
                                                f"{label} {cc}: area ratio with outlet volume {to_cc} cell {to_cell} exceeds 10:1 (ratio={ratio:.1f})"
                                            )
                    except Exception:
                        pass
        except Exception:
            pass
            
    # 3. Check heat structures
    try:
        fn = getattr(model, "heatstructs", None)
        if fn is not None:
            comps = _coerce_list(fn())
            for comp in comps:
                cc = _get_cc(comp)
                
                # Check left and right boundary cell references
                for face in ("left", "right"):
                    try:
                        face_list = getattr(comp, face, None)
                        if face_list is not None:
                            for idx in range(len(face_list)):
                                try:
                                    bcell = face_list[idx].bcell
                                    ref = bcell.reference
                                    if ref is None or str(ref).strip() in ("", "0", "0000000"):
                                        warnings.append(
                                            f"Heat Structure {cc} cell {idx + 1} {face} boundary is unconnected (insulated)"
                                        )
                                except Exception:
                                    pass
                    except Exception:
                        pass
    except Exception:
        pass
        
    return errors, warnings


def _run_validation(model) -> tuple[list[str], list[str]]:
    """Run SNAP's built-in validation checks along with Python-level checks."""
    errors: list[str] = []
    warnings: list[str] = []
    java_model = model.java_model

    # 1. Validation tests via reflection (equivalent to GUI checks like loops/trips)
    try:
        tests = java_model.getValidationTests()
        for test in tests:
            try:
                test.runValidation(False)
                display = str(test.getDisplayName())
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

    # 2. Redirect static Message stream to capture component and option errors/warnings
    try:
        from py4j.java_gateway import JavaGateway
        jvm = JavaGateway(gateway_client=java_model._gateway_client).jvm
        Message = jvm.com.cafean.client.ui.message.Message
        baos = jvm.java.io.ByteArrayOutputStream()
        ps = jvm.java.io.PrintStream(baos)
        original = Message.getOutputStream()
        Message.setOutputStream(ps)
        try:
            # Validate model options (e.g. missing Time Step cards)
            try:
                opts = model.model_options()
                if opts is not None and hasattr(opts, "java_object"):
                    opts.java_object.isOkayForExport(True)
            except Exception:
                pass

            # Validate all components
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
                    if "Error:" in line:
                        errors.append(line)
                    else:
                        warnings.append(line)
    except Exception as exc:
        warnings.append(f"[component stream check unavailable: {exc}]")

    # Supplement with Python-level checks
    py_errors, py_warnings = _python_model_check(model)
    errors.extend(py_errors)
    warnings.extend(py_warnings)

    return errors, warnings


def register_export_tools(mcp) -> None:

    @mcp.tool()
    def validate_model(model_id: str) -> dict:
        """Run SNAP's built-in model check and return any validation errors or warnings.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: valid (bool), errors (list[str]), warnings (list[str])
        """
        model = _session.get(model_id)
        errors, warnings = _run_validation(model)
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    @mcp.tool()
    def review_model(model_id: str) -> dict:
        """Audit a model: component inventory, connection topology, and validation issues.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: model_id, n_components, components (list), connections (list),
                        issues (list), issue_count (int), clean (bool)
        """
        model = _session.get(model_id)
        
        components = []
        connections = []
        
        for ctype, cfg in COMPONENT_MAP.items():
            try:
                getter = getattr(model, cfg["list"])
                items = _coerce_list(getter())
                for item in items:
                    cc = _get_cc(item)
                    name = ""
                    try:
                        name = str(item.name)
                    except Exception:
                        pass
                    
                    components.append({
                        "type": ctype,
                        "number": cc,
                        "name": name
                    })
                    
                    # Connection info for junctions
                    if ctype in ("SINGLE_JUNCTION", "TIME_DEPENDENT_JUNCTION", "VALVE", "PUMP"):
                        for face in ("inlet", "outlet"):
                            try:
                                val = getattr(item, face, None)
                                if val is not None and str(val).strip() not in ("", "0", "0000000"):
                                    connections.append({
                                        "component_number": cc,
                                        "component_type": ctype,
                                        "face": face,
                                        "connection": str(val)
                                    })
                            except Exception:
                                pass
            except Exception:
                pass
                
        errors, warnings = _run_validation(model)
        issues = errors + warnings
        
        return {
            "model_id": model_id,
            "n_components": len(components),
            "components": sorted(components, key=lambda c: (c["type"], c["number"])),
            "connections": connections,
            "issues": issues,
            "issue_count": len(issues),
            "clean": len(errors) == 0
        }

    @mcp.tool()
    def export_relap(
        model_id: str,
        path: str,
        force: bool = False,
    ) -> dict:
        """Export the model to a RELAP5 ASCII input deck (.inp).

        Parameters
        ----------
        model_id : str
        path : str
            Full output path for the .inp file.
        force : bool, default False
            If True, validation errors are bypassed and export proceeds regardless.
            Use with caution.

        Returns
        -------
        dict with keys: status (str), exported_files (list[str])
        """
        model = _session.get(model_id)
        
        # Enforce validation (unless force is True)
        errors, warnings = _run_validation(model)
        if errors and not force:
            return {
                "status": "error",
                "error": "Model validation failed. You must fix these errors before exporting (or set force=true).",
                "errors": errors,
                "warnings": warnings,
                "exported_files": [],
            }
            
        import pathlib
        path_obj = pathlib.Path(path)
        result = model.export(path_obj)
        if result is None:
            return {
                "status": "error",
                "exported_files": [],
                "error": "Export returned None — check model for errors",
            }
        
        exported_files = []
        if isinstance(result, list):
            for es in result:
                locs = getattr(es, 'locations', None) or []
                exported_files.extend([str(p) for p in locs])
        else:
            locs = getattr(result, 'locations', None)
            loc = getattr(result, 'location', None)
            if locs:
                exported_files = [str(p) for p in locs]
            elif loc:
                exported_files = [str(loc)]
            else:
                exported_files = [path]
        return {"status": "ok", "exported_files": exported_files}

    @mcp.tool()
    def save_med(
        model_id: str,
        path: str,
        force: bool = False,
    ) -> dict:
        """Save the current model state as a SNAP .med file.

        Parameters
        ----------
        model_id : str
        path : str
            Full output path for the .med file.
        force : bool, default False
            If True, validation errors are bypassed and save proceeds regardless.

        Returns
        -------
        dict with keys: status (str), path (str)
        """
        model = _session.get(model_id)
        
        # Enforce validation (unless force is True)
        errors, warnings = _run_validation(model)
        if errors and not force:
            return {
                "status": "error",
                "error": "Model validation failed. You must fix these errors before saving (or set force=true).",
                "errors": errors,
                "warnings": warnings,
            }
            
        try:
            model.save(path)
        except AttributeError:
            try:
                model.save_as(path)
            except AttributeError:
                model.java_model.save(path)
        return {"status": "ok", "path": path}
