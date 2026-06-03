"""Model-level tools: status, create, import, open, list."""

from __future__ import annotations
import os
import tempfile
import uuid

from snap_melcor import session as _session


def register_model_tools(mcp) -> None:

    @mcp.tool()
    def melcor_status() -> dict:
        """Check that the MELCOR2X SNAP plugin is loaded and return its version.

        Returns
        -------
        dict with keys: plugin_loaded (bool), version (str | None),
                        open_models (list[str])
        """
        try:
            import snap.codes.melcor as _mc  # noqa: F401
            import snap.utils.version as _ver
            version = str(_ver.get_plugin_version("melcor2x.jar"))
        except Exception as exc:
            return {"plugin_loaded": False, "error": str(exc), "open_models": []}

        return {
            "plugin_loaded": True,
            "version": version,
            "open_models": _session.list_ids(),
        }

    @mcp.tool()
    def create_model(title: str = "New Model") -> dict:
        """Create a new empty MELCOR model session.

        MELCOR has no "blank canvas" API — a minimal MELGEN input is generated
        internally and imported to bootstrap the model. The returned model_id
        is used in all subsequent tool calls.

        Parameters
        ----------
        title : str
            Model title string (written into the MELGEN TITLE card).

        Returns
        -------
        dict with keys: model_id (str), status (str), title (str)
        """
        import snap.codes.melcor as _mc

        minimal_inp = f"TITLE\n{title}\n"
        fd, tmp_path = tempfile.mkstemp(suffix=".inp")
        try:
            with os.fdopen(fd, "w") as f:
                f.write(minimal_inp)
            model = _mc.import_melgen(tmp_path)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        if model is None:
            return {"model_id": None, "status": "error",
                    "error": "import_melgen returned None"}

        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok", "title": title}

    @mcp.tool()
    def import_melgen(path: str) -> dict:
        """Import a MELGEN ASCII input file (.inp) and open it as a model session.

        Parameters
        ----------
        path : str
            Full path to the MELGEN 2.x input file.

        Returns
        -------
        dict with keys: model_id (str), status (str)
        """
        import snap.codes.melcor as _mc

        model = _mc.import_melgen(path)
        if model is None:
            return {
                "model_id": None,
                "status": "error",
                "error": f"import_melgen returned None for path: {path}",
            }
        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok"}

    @mcp.tool()
    def open_med_model(path: str) -> dict:
        """Open an existing MELCOR .med file.

        Parameters
        ----------
        path : str
            Full path to the .med file.

        Returns
        -------
        dict with keys: model_id (str), status (str)
        """
        # snap.codes.melcor.open_model() checks for "MELCOR" but the plugin ID
        # is "MELCOR2X" — use snap.model_editor.open_model() directly instead.
        import snap.model_editor as me

        try:
            model = me.open_model(path)
        except (FileNotFoundError, ValueError) as exc:
            return {"model_id": None, "status": "error", "error": str(exc)}

        model_id = uuid.uuid4().hex[:8]
        _session.register(model_id, model)
        return {"model_id": model_id, "status": "ok"}

    @mcp.tool()
    def list_models() -> list[str]:
        """Return the IDs of all currently open MELCOR model sessions."""
        return _session.list_ids()

    @mcp.tool()
    def close_model(model_id: str) -> dict:
        """Close an open MELCOR model session and release its resources.

        Parameters
        ----------
        model_id : str
            Session ID from create_model / import_melgen / open_med_model.

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        try:
            model.close()
        except Exception as exc:
            return {"status": "error", "error": str(exc)}
        _session.remove(model_id)
        return {"status": "ok", "model_id": model_id}
