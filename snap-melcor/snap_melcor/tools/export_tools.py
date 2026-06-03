"""Validation and export tools."""

from __future__ import annotations

from snap_melcor import session as _session


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
            # validate() may not exist on MelcorModel — fall back to export check
            try:
                import tempfile, os
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

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    @mcp.tool()
    def export_melgen(model_id: str, path: str) -> dict:
        """Export the model to a MELGEN ASCII input file.

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
        # result is MEDExportSet or list[MEDExportSet]
        if isinstance(result, list):
            exported_files = []
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
