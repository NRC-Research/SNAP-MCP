"""SNAP-TRACE MCP Server — entry point.

Exposes TRACE input deck generation through the Model Context Protocol.
SNAP's Python API (snap.codes.trace) is used directly; MEBatch/py4j starts
automatically in the background when this module loads.

Configuration (environment variables):
  SNAP_PYTHON_PATH    path to SNAP's python directory
                      default: ~/run-snap500/python
  SNAP_TRACE_DB       path to the SQLite model registry
                      default: ~/.snap_trace/models.db
  SNAP_TRACE_WORKDIR  directory for auto-saved .med files
                      default: ~/.snap_trace/models/
  SNAP_MCP_STARTUP_WAIT
                      seconds a tool waits for MEBatch to finish starting
                      before failing; default: 90
"""
import sys
import os
import logging
import functools
import threading
# Log to BOTH stderr (for the MCP client) and a file we can read out-of-band, so
# gateway-break exceptions are diagnosable even when the client swallows stderr.
_logdir = os.path.expanduser("~/.snap_trace")
try:
    os.makedirs(_logdir, exist_ok=True)
    _handlers = [logging.StreamHandler(sys.stderr),
                 logging.FileHandler(os.path.join(_logdir, "server.log"))]
except Exception:
    _handlers = [logging.StreamHandler(sys.stderr)]
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s pid=%(process)d %(name)s %(levelname)s %(message)s",
                    handlers=_handlers)
_log = logging.getLogger("mcp_server")

# Save real stdout before SNAP imports it — snap.streams replaces sys.stdout
# with a _StreamLogHandler, which breaks MCP's stdio transport (.buffer lookup).
_real_stdout = sys.stdout

# Import snap_env FIRST so SNAP path is on sys.path before any snap.* imports
# and so MEBatch starts in the background immediately.
import snap_trace.snap_env as snap_env  # noqa: F401 — side-effectful import

from mcp.server.fastmcp import FastMCP

from snap_trace.tools import (
    model_tools,
    component_tools,
    connection_tools,
    export_tools,
    v2v_tools,
)
import snap_trace.resources as resources

mcp = FastMCP(
    "snap-trace",
    instructions=(
        "Build TRACE thermal-hydraulic input decks using SNAP's native Python API. "
        "Tool names below are written bare, but many MCP clients expose them with a "
        "prefix (e.g. 'mcp_snap_trace_create_model'). Always call tools by the exact "
        "name your client lists, never by the bare name written here. "
        "Begin by creating a model (create_model) or opening an existing one "
        "(open_med_model / import_trcin); tools wait for SNAP automatically, so there "
        "is no need to poll snap_status first. "
        "Always read a component's schema (get_component_schema) before adding a new "
        "component type — schemas include NRC modeling guidance defaults (dxin, volin, "
        "epsw, material numbers, radial node counts). "
        "For VESSEL components attach 1-D pipes with connect_pipe_to_vessel — "
        "connect_components uses 1-D junction labels that the VESSEL API rejects. "
        "Initialize VESSEL per-cell ICs (p, tl, tv, alp) and edge hydraulic diameters "
        "(hd_axial, hd_azimuthal, hd_radial) with set_vessel_table — "
        "these tables are not reachable via set_component_property. "
        "For vessel-in-vessel Cartesian core models use compute_vessel_junctions "
        "to generate the VESSEL junction Connection Edge Data from the core layout. "
        "A clean validate_model result is NOT proof the deck runs: TRACE applies "
        "checks SNAP does not, so confirm with run_trace before reporting success. "
        "See trace://workflow/analyst-guidance for scope and best practices. "
        "See trace://workflow/new-model for a step-by-step build guide. "
        "NRC TRACE modeling guidance: https://nrc-research.github.io/TRACE_guidance/"
    ),
)

# Register all tools and resources
model_tools.register(mcp)
component_tools.register(mcp)
connection_tools.register(mcp)
export_tools.register(mcp)
v2v_tools.register(mcp)
resources.register(mcp)


# Serialize ALL tool calls onto the single Py4J/MEBatch gateway. The gateway
# (one socket to one JVM) is NOT thread-safe, and FastMCP dispatches sync tools
# on a worker-thread pool — so a client that fires tool calls concurrently
# without waiting (e.g. some agents) puts two requests on the socket at once,
# interleaving the protocol and corrupting the gateway ('NoneType' has no
# attribute 'findPlugin'). Well-behaved clients (Claude, Copilot) serialize
# their calls and never hit this; this lock makes the server robust regardless.
_GATEWAY_LOCK = threading.Lock()

# Tools that do NOT touch the Py4J gateway and must work during init/reset
# (so a caller can poll readiness). Everything else waits for MEBatch to come
# up — see the wait in _make_reconnect_wrapper.
_ALWAYS_ALLOWED = {"snap_status", "compute_vessel_junctions"}

# How long a gateway-touching tool will wait for MEBatch before giving up.
# A cold MEBatch start is ~12-20 s; a reset() relaunch is comparable. This is
# the ceiling on a genuinely stuck start, not the expected wait.
_STARTUP_WAIT = float(os.environ.get("SNAP_MCP_STARTUP_WAIT", "90"))

_INITIALIZING_MSG = (
    "SNAP/MEBatch did not become ready within {seconds}s, so this tool could "
    "not run. This means startup failed, not that you called too early — "
    "retrying immediately will not help. Call snap_status() to see the error. "
    "Detail: {detail}"
)


def _make_reconnect_wrapper(fn, is_async: bool):
    """Wrap a tool function so Py4J gateway failures trigger auto-reconnect."""
    _MSG = (
        "SNAP/Py4J gateway connection was broken and has been reset. "
        "All in-memory model state was cleared. "
        "Wait ~15 seconds for MEBatch to restart, then call snap_status() to confirm "
        "ready=true, then recreate or reopen the model before continuing."
    )
    if is_async:
        @functools.wraps(fn)
        async def _async_wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except Exception as exc:
                if snap_env.is_connection_broken(exc):
                    snap_env.reset()
                    raise RuntimeError(_MSG) from None
                raise
        return _async_wrapper
    else:
        @functools.wraps(fn)
        def _sync_wrapper(*args, **kwargs):
            # Never touch the gateway while MEBatch is (re)initializing: that
            # races the background init thread, and a flood of queued calls each
            # tripping reset() piles up dead MEBatch JVMs and wedges it.
            #
            # Block until the init thread signals ready rather than telling the
            # caller to poll. An LLM agent has no clock and no sleep tool, so
            # "wait 15 seconds and retry" is an instruction it cannot follow: it
            # spends its whole turn budget re-calling snap_status() and gives up
            # having done nothing. Waiting here is also strictly safer than the
            # old immediate raise — a waiting call is parked on an event, so it
            # cannot reach the gateway or trip reset() while init is in flight.
            if fn.__name__ not in _ALWAYS_ALLOWED and not snap_env.is_ready():
                ready, err = snap_env.wait_ready(_STARTUP_WAIT)
                if not ready:
                    raise RuntimeError(_INITIALIZING_MSG.format(
                        seconds=int(_STARTUP_WAIT),
                        detail=err or "no further detail available",
                    ))
            try:
                with _GATEWAY_LOCK:
                    return fn(*args, **kwargs)
            except Exception as exc:
                if snap_env.is_connection_broken(exc):
                    # Log the REAL exception (and which tool) so we can find why
                    # the gateway breaks — the user sees only the generic message.
                    _log.error("GATEWAY BROKE during tool '%s' args=%r kwargs=%r: %r",
                               fn.__name__, args, kwargs, exc, exc_info=True)
                    snap_env.reset()
                    raise RuntimeError(_MSG) from None
                raise
        return _sync_wrapper


# Wrap every registered tool so Py4J gateway failures auto-reset MEBatch.
for _tool in mcp._tool_manager._tools.values():
    _tool.fn = _make_reconnect_wrapper(_tool.fn, _tool.is_async)


def main():
    # Restore real stdout so MCP's stdio transport can access sys.stdout.buffer.
    # SNAP's streams_init replaces sys.stdout with a _StreamLogHandler on import.
    sys.stdout = _real_stdout
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
