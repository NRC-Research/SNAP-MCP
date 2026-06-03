"""MCP tools: model lifecycle (create, open, import, list, status)."""
from __future__ import annotations

from pathlib import Path

import snap_trace.snap_env as snap_env
import snap_trace.session as session

_DEFAULT_VERSION = snap_env.SNAP_TRACE_TARGET_VERSION


def register(mcp):

    @mcp.tool()
    def snap_status() -> dict:
        """Return the current status of the SNAP/TRACE connection.

        Call this first if you are unsure whether SNAP has finished
        initializing. 'ready: true' means all tools are usable.
        'initializing: true' means MEBatch is still starting up (wait ~15 s).

        Returns snap_plugin_version (the TRACE plugin version SNAP was built
        against) and target_trace_version (the TRACE binary version you are
        exporting for, set via SNAP_TRACE_TARGET_VERSION env var).  Export
        fixups are applied based on target_trace_version.
        """
        return snap_env.status()

    @mcp.tool()
    def create_model(name: str, version: str = _DEFAULT_VERSION) -> dict:
        """Create a new, empty TRACE model.

        Parameters
        ----------
        name : str
            Human-readable name for the model.
        version : str
            TRACE code version string (e.g. "V5.0p5", "V5.0p9").
            Defaults to SNAP_TRACE_TARGET_VERSION env var (currently
            {_DEFAULT_VERSION}).

        Returns
        -------
        dict with model_id, name, version.
        The model_id is used in all subsequent tool calls.
        """
        snap_env.wait_ready()
        model_id, _ = session.create_model(name, version)
        return {"model_id": model_id, "name": name, "version": version}

    @mcp.tool()
    def list_models() -> list[dict]:
        """List all models tracked in this session (persisted across restarts)."""
        return session.list_models()

    @mcp.tool()
    def open_med_model(med_file_path: str, name: str = "") -> dict:
        """Open an existing SNAP .med model file.

        Parameters
        ----------
        med_file_path : str
            Absolute path to the .med file.
        name : str
            Optional display name (defaults to the file stem).

        Returns
        -------
        dict with model_id and component_count.
        """
        snap_env.wait_ready()
        import snap.codes.trace as trace
        model = trace.open_model(med_file_path)
        display = name or Path(med_file_path).stem
        model_id, _ = session.register_model(display, model, med_file_path)
        from snap_trace.component_map import iter_all_components
        count = len(iter_all_components(model))
        return {"model_id": model_id, "name": display, "component_count": count}

    @mcp.tool()
    def import_trcin(trcin_path: str, name: str = "",
                     version: str | None = None) -> dict:
        """Import an existing TRACE ASCII input deck (.inp / .trcin).

        Parameters
        ----------
        trcin_path : str
            Absolute path to the TRACE input file.
        name : str
            Optional display name.
        version : str | None
            Target TRACE version, or None for auto-detect.

        Returns
        -------
        dict with model_id and component_count.
        """
        snap_env.wait_ready()
        import snap.codes.trace as trace
        model = trace.import_ascii(trcin_path, version)
        display = name or Path(trcin_path).stem
        model_id, _ = session.register_model(display, model, trcin_path)
        from snap_trace.component_map import iter_all_components
        count = len(iter_all_components(model))
        return {"model_id": model_id, "name": display, "component_count": count}
