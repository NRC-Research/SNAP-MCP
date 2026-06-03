"""Validation and export tools."""

from __future__ import annotations
import tempfile
import os

from snap_relap import session as _session


def _python_model_check(model) -> tuple[list[str], list[str]]:
    """Perform Python-level validation check for unconnected junctions and heat structures."""
    errors = []
    warnings = []
    
    # 1. Check junctions (SINGLE_JUNCTION, TIME_DEPENDENT_JUNCTION, VALVE, PUMP)
    junction_getters = [
        ("single_junctions", "Single Junction"),
        ("time_dependent_junctions", "Time Dependent Junction"),
        ("valves", "Valve"),
        ("pumps", "Pump"),
    ]
    
    from snap_relap.component_map import _coerce_list
    
    for getter, label in junction_getters:
        try:
            fn = getattr(model, getter, None)
            if fn is not None:
                comps = _coerce_list(fn())
                for comp in comps:
                    cc = -1
                    for attr in ("getCCnumber", "number", "getComponentNumber"):
                        try:
                            v = getattr(comp, attr)
                            cc = int(v() if callable(v) else v)
                            break
                        except Exception:
                            pass
                    
                    # Check inlet
                    try:
                        inlet = getattr(comp, "inlet", None)
                        if inlet is None or str(inlet).strip() in ("", "0", "0000000"):
                            errors.append(f"{label} {cc}: inlet is unconnected")
                    except Exception:
                        pass
                        
                    # Check outlet
                    try:
                        outlet = getattr(comp, "outlet", None)
                        if outlet is None or str(outlet).strip() in ("", "0", "0000000"):
                            errors.append(f"{label} {cc}: outlet is unconnected")
                    except Exception:
                        pass
        except Exception:
            pass
            
    # 2. Check heat structures
    try:
        fn = getattr(model, "heatstructs", None)
        if fn is not None:
            comps = _coerce_list(fn())
            for comp in comps:
                cc = -1
                for attr in ("getCCnumber", "number", "getComponentNumber"):
                    try:
                        v = getattr(comp, attr)
                        cc = int(v() if callable(v) else v)
                        break
                    except Exception:
                        pass
                
                # Check left and right boundary cell references
                for face in ("left", "right"):
                    try:
                        face_list = getattr(comp, face, None)
                        if face_list is not None:
                            # face_list is list of boundary cell objects
                            for idx in range(len(face_list)):
                                try:
                                    bcell = face_list[idx].bcell
                                    ref = bcell.reference
                                    if ref is None or str(ref).strip() in ("", "0", "0000000"):
                                        # Warn that it's unconnected
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


def register_export_tools(mcp) -> None:

    @mcp.tool()
    def validate_model(model_id: str) -> dict:
        """Run SNAP's built-in model validation and return errors and warnings.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with keys: valid (bool), errors (list[str]), warnings (list[str])
        """
        model = _session.get(model_id)
        java_model = model.java_model
        errors: list[str] = []
        warnings: list[str] = []

        try:
            messages = java_model.validate()
            for msg in (messages or []):
                text = str(msg)
                if 'ERROR' in text.upper():
                    errors.append(text)
                else:
                    warnings.append(text)
        except AttributeError:
            # Fall back to export validation check if validate method is missing
            try:
                with tempfile.NamedTemporaryFile(suffix='.inp', delete=False) as f:
                    tmp_path = f.name
                result = model.export(tmp_path)
                os.unlink(tmp_path)
                if result is None:
                    errors.append("Export returned None — model likely has errors")
            except Exception as exc:
                errors.append(f"Validation via export failed: {exc}")
        except Exception as exc:
            errors.append(f"Validation failed: {exc}")

        # Supplement with Python-level checks
        py_errors, py_warnings = _python_model_check(model)
        errors.extend(py_errors)
        warnings.extend(py_warnings)

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    @mcp.tool()
    def export_relap(model_id: str, path: str) -> dict:
        """Export the model to a RELAP5 ASCII input deck (.inp).

        Parameters
        ----------
        model_id : str
        path : str
            Full output path for the .inp file.

        Returns
        -------
        dict with keys: status (str), exported_files (list[str])
        """
        model = _session.get(model_id)
        result = model.export(path)
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
    def save_med(model_id: str, path: str) -> dict:
        """Save the current model state as a SNAP .med file.

        Parameters
        ----------
        model_id : str
        path : str
            Full output path for the .med file.

        Returns
        -------
        dict with keys: status (str), path (str)
        """
        model = _session.get(model_id)
        try:
            model.save(path)
        except AttributeError:
            try:
                model.save_as(path)
            except AttributeError:
                model.java_model.save(path)
        return {"status": "ok", "path": path}
