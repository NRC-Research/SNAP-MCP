"""Bootstrap the SNAP Python path and initialize the MEBatch/py4j connection.

This module must be imported before any snap.* imports. It inserts the SNAP
python directory into sys.path so that snap.codes.trace and py4j are found,
then eagerly starts the MEBatch process so the first tool call has no delay.
"""
import atexit
import os
import re
import signal
import subprocess
import sys
import threading
import logging
from typing import Optional, Tuple

log = logging.getLogger(__name__)

# On Windows the MCP server runs under pythonw.exe (no console), so any console
# child SNAP's launcher spawns (MEBatch.exe / the py4j JVM) allocates a NEW
# console and a visible black window pops up on the user's desktop. SNAP's own
# code does the spawning, so default every Popen in THIS process to
# CREATE_NO_WINDOW before snap.* is imported. Pipes (py4j's port handshake)
# are unaffected; callers that explicitly ask for a console still get one.
if sys.platform == "win32":
    _OrigPopen = subprocess.Popen

    class _NoWindowPopen(_OrigPopen):
        def __init__(self, *args, **kwargs):
            flags = kwargs.get("creationflags", 0) or 0
            if not flags & subprocess.CREATE_NEW_CONSOLE:
                kwargs["creationflags"] = flags | subprocess.CREATE_NO_WINDOW
            super().__init__(*args, **kwargs)

    subprocess.Popen = _NoWindowPopen

SNAP_PYTHON = os.environ.get("SNAP_PYTHON_PATH", "")
if not SNAP_PYTHON:
    raise RuntimeError(
        "SNAP_PYTHON_PATH environment variable is not set. "
        "Find the correct path with: "
        "find ~ /opt/snap -name 'model_editor.py' 2>/dev/null"
    )

if SNAP_PYTHON not in sys.path:
    sys.path.insert(0, SNAP_PYTHON)

# Target TRACE version — controls which export fixups are applied and the
# default version used when creating new models.  Set via the
# SNAP_TRACE_TARGET_VERSION env var.  Format: "V5.0p9", "V5.0p10", etc.
SNAP_TRACE_TARGET_VERSION: str = os.environ.get(
    "SNAP_TRACE_TARGET_VERSION", "V5.0p9"
)


def parse_version(vstr: str) -> Tuple[int, int, int]:
    """Parse "V5.0p9" → (5, 0, 9).  Returns (0, 0, 0) on parse failure."""
    m = re.match(r"[Vv]?(\d+)\.(\d+)[pP](\d+)", vstr)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return (0, 0, 0)


def target_version() -> Tuple[int, int, int]:
    return parse_version(SNAP_TRACE_TARGET_VERSION)


# ── connection state ──────────────────────────────────────────────────────────
_ready = False
_error: Optional[str] = None
_plugin_version: Optional[str] = None
_lock = threading.Lock()
# Single-flight launcher lock: only one _start loop may run at a time. reset()
# and status() can each spawn a _start thread; if two run concurrently they each
# launch a MEBatch and then kill the OTHER's in-flight JVM via _kill_own_mebatch
# (SIGKILL → "Model Editor exited with code 137"), so no launch ever completes.
_start_lock = threading.Lock()


def _start() -> None:
    """Single-flight wrapper around the MEBatch connection loop.

    Skips immediately if another _start loop already holds the launcher lock,
    so concurrent init/reset/status threads can't fight over MEBatch launches.
    """
    if not _start_lock.acquire(blocking=False):
        log.info("_start already in progress — skipping duplicate launcher")
        return
    try:
        _start_loop()
    finally:
        _start_lock.release()


def _start_loop() -> None:
    """Connect to SNAP/MEBatch, retrying until TRACE plugin is loaded.

    Two distinct failure modes require different handling:
      - AttributeError: 'NoneType' has no attribute 'findPlugin' — the Py4J
        gateway entry_point is null (import succeeded but gateway never connected).
        Fix: evict snap.model_editor from sys.modules so the next iteration does
        a fresh import that reconnects or restarts MEBatch.
      - RuntimeError / find_plugin returns None — MEBatch is running but the
        TRACE plugin registry isn't populated yet.  Fix: just wait and retry
        find_plugin() on the same me object.
    """
    global _ready, _error, _plugin_version
    import time as _time

    _max_attempts = 15
    _retry_delay  = 8.0   # seconds between attempts

    for attempt in range(1, _max_attempts + 1):
        # Import snap.model_editor — uses cached module if available, or does a
        # fresh import (starting MEBatch) if the previous iteration evicted it.
        try:
            import snap.model_editor as me
        except Exception as exc:
            _error = f"snap.model_editor import failed: {exc}"
            log.error("snap.model_editor import failed on attempt %d: %s", attempt, exc)
            if attempt < _max_attempts:
                _time.sleep(_retry_delay)
            continue

        try:
            plugin = me.find_plugin("TRACE")
            if plugin is None:
                raise RuntimeError(
                    "find_plugin('TRACE') returned None — "
                    "MEBatch is running but TRACE plugin not yet loaded"
                )
            for attr in ("getVersion", "version", "getPluginVersion", "pluginVersion"):
                try:
                    val = getattr(plugin, attr)
                    _plugin_version = str(val() if callable(val) else val)
                    break
                except Exception:
                    pass
            _ready = True
            _error = None
            log.info(
                "SNAP/TRACE connection established on attempt %d (plugin version: %s)",
                attempt, _plugin_version,
            )
            return
        except Exception as exc:
            msg = str(exc)
            # findPlugin/AttributeError means SNAP's model-editor singleton is
            # stuck "active" while its java_interface points at a dead gateway,
            # so find_plugin keeps calling None.findPlugin. VALIDATED fix: just
            # shutdown() the singleton — that resets is_active() to False so the
            # NEXT find_plugin re-activates it, which relaunches MEBatch cleanly
            # in the same process. Do NOT kill JVMs or evict modules here: those
            # killed the in-flight relaunch / corrupted py4j state and caused the
            # permanent wedge. (The benign "TRACE already loaded" line in the
            # MEBatch log is unrelated — it appears on every launch, success too.)
            if isinstance(exc, AttributeError) or "findPlugin" in msg:
                _error = f"Py4J gateway broken (attempt {attempt}/{_max_attempts}): {exc}"
                log.warning(
                    "Gateway dead on attempt %d — resetting singleton to relaunch: %s",
                    attempt, exc,
                )
                try:
                    me.__MODEL_EDITOR__.shutdown()
                except Exception:
                    pass
            else:
                _error = msg
                log.warning(
                    "SNAP/TRACE startup attempt %d/%d failed: %s",
                    attempt, _max_attempts, exc,
                )
            if attempt < _max_attempts:
                _time.sleep(_retry_delay)

    log.error("SNAP/TRACE startup failed after %d attempts: %s", _max_attempts, _error)


def _ppid_of(pid):
    """Parent PID from /proc, robust to comm fields containing spaces/parens."""
    try:
        with open(f"/proc/{pid}/stat") as fh:
            return int(fh.read().rsplit(")", 1)[1].split()[1])
    except Exception:
        return None


def _pgrep_f(pattern):
    import subprocess as _sp
    try:
        out = _sp.run(["pgrep", "-f", pattern], capture_output=True,
                      text=True, timeout=5)
        return [int(x) for x in out.stdout.split()]
    except Exception:
        return []


def _mebatch_pids():
    return _pgrep_f("MEBatch")


def _reaches_ancestor(pid, roots) -> bool:
    """True if pid's parent chain reaches any pid in ``roots``."""
    roots = set(roots)
    cur, hops = _ppid_of(pid), 0
    while cur and cur > 1 and hops < 12:
        if cur in roots:
            return True
        cur, hops = _ppid_of(cur), hops + 1
    return False


def _reap_orphan_mebatch() -> None:
    """Reap leftover MEBatch JVMs from dead servers — never live tenants'.

    A blanket ``pkill -f MEBatch`` kills EVERY MEBatch JVM owned by this user,
    including those belonging to other *running* snap-trace MCP servers sharing
    this host (e.g. a concurrent crush or Copilot instance). That severs their
    Py4J gateway and leaves them stuck with
    ``'NoneType' object has no attribute 'findPlugin'``.

    Instead, only kill a MEBatch process whose ancestor chain does NOT reach a
    still-running mcp_server.py — i.e. true orphans from a crashed/restarted
    server. Live tenants (including this process's own future MEBatch) are
    spared. This still prevents the idle-JVM accumulation the old code targeted,
    because a server's MEBatch is reparented away from its python on exit and
    becomes reapable on the next start.
    """
    import subprocess as _sp
    try:
        live_servers = set(_pgrep_f("SNAP-MCP/mcp_server.py"))
        for pid in _mebatch_pids():
            if not _reaches_ancestor(pid, live_servers):
                _sp.run(["kill", "-9", str(pid)], capture_output=True)
        import time as _t; _t.sleep(2)  # let the OS free the Py4J port
    except Exception:
        pass


def _kill_own_mebatch() -> None:
    """Kill ONLY this process's own MEBatch JVM(s).

    Used by reset() to bounce a broken gateway. Never a global
    ``pkill -f MEBatch`` — that would tear down every other live snap-trace
    server's MEBatch on this host and cascade gateway-broken errors across
    crush / Copilot / Claude instances.
    """
    import os as _os, subprocess as _sp
    self_pid = _os.getpid()
    try:
        for pid in _mebatch_pids():
            if _reaches_ancestor(pid, {self_pid}):
                _sp.run(["kill", "-9", str(pid)], capture_output=True)
    except Exception:
        pass


def _shutdown_mebatch(signum=None, frame=None) -> None:
    """Tear down our MEBatch JVM when this server exits.

    Without this the JVM outlives the MCP process. That is not merely untidy:
    an MCP client waits on its server's process tree, so a surviving JVM hangs
    the client's shutdown indefinitely. Observed with crush -- the run finished
    its work in 17 seconds and then sat for over two hours at 0% CPU with an
    orphaned JVM alive, which reads as a hung agent rather than a completed one.

    Only ever kills JVMs descended from this process (see _kill_own_mebatch),
    so concurrent snap-trace servers are unaffected.
    """
    _kill_own_mebatch()
    if signum is not None:
        # Re-raise with the default handler so the exit status is honest.
        try:
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)
        except Exception:
            pass


atexit.register(_shutdown_mebatch)

# SIGTERM/SIGINT are how a client stops its MCP server; without handlers the
# atexit hook never runs. signal() only works on the main thread, so tolerate
# failure rather than breaking import in a threaded host.
for _sig in (signal.SIGTERM, signal.SIGINT):
    try:
        signal.signal(_sig, _shutdown_mebatch)
    except (ValueError, OSError, AttributeError):
        pass

_reap_orphan_mebatch()

# Fire off the MEBatch startup in a background thread immediately.
_thread = threading.Thread(target=_start, daemon=True, name="snap-init")
_thread.start()


def wait_ready(timeout: float = 60.0) -> Tuple[bool, Optional[str]]:
    """Block until MEBatch is up or the timeout expires.

    Returns (ready, error_message).
    """
    _thread.join(timeout=timeout)
    return _ready, _error


def status() -> dict:
    global _thread
    # If the init thread died without becoming ready, restart it so the LLM
    # can poll snap_status() and eventually get ready=true without restarting
    # the entire MCP server process.
    if not _ready and not _thread.is_alive():
        log.info("snap_status(): restarting failed init thread")
        _thread = threading.Thread(target=_start, daemon=True, name="snap-retry")
        _thread.start()
    initializing = _thread.is_alive()
    return {
        "ready": _ready,
        "initializing": initializing,
        "error": _error,
        "snap_python_path": SNAP_PYTHON,
        "snap_plugin_version": _plugin_version,
        "target_trace_version": SNAP_TRACE_TARGET_VERSION,
    }


def is_ready() -> bool:
    """True when MEBatch/TRACE is connected and tool calls may touch the gateway.

    Tool wrappers check this to fail fast while the background init/reset thread
    is bringing MEBatch up — touching the non-thread-safe gateway during that
    window races the init thread and corrupts it.
    """
    return _ready


def is_connection_broken(exc: Exception) -> bool:
    """Return True ONLY for a genuinely dead/corrupted Py4J gateway.

    Critical: a Py4JJavaError means the gateway successfully relayed a Java-side
    exception — i.e. the gateway is HEALTHY and a tool/modeling call simply
    failed (e.g. an invalid setJun2 connection). That must NOT trigger a reset.
    The old code matched the substring "GatewayConnection", which appears in the
    "at py4j.GatewayConnection.run" frame of EVERY Py4JJavaError traceback, so
    every routine Java error was misread as a dead gateway and forced a pointless
    MEBatch relaunch — the "constant gateway breaks" under a client that makes
    many failing calls. Only true network/connection failures are real breaks.
    """
    try:
        from py4j.protocol import Py4JJavaError
        if isinstance(exc, Py4JJavaError):
            return False
    except Exception:
        pass
    msg = str(exc)
    return (
        "Py4JNetworkError" in msg
        or "Unknown command" in msg
        or "trying to connect to the Java server" in msg
        or "An error occurred while trying to connect" in msg
        or "Connection refused" in msg
        or "Broken pipe" in msg
    )


def reset() -> None:
    """Recover from a broken Py4J gateway by relaunching MEBatch in-process.

    Validated recovery: shut down SNAP's model-editor singleton (which resets
    is_active() to False) and let the connection thread call find_plugin, which
    re-activates the singleton and relaunches MEBatch in the same process. After
    reset() the module-level _ready flag is False until MEBatch is back up;
    callers should raise a user-visible "retry after snap_status" error.

    Deliberately does NOT kill JVMs or evict snap/py4j modules — both sabotage
    the relaunch (kill the in-flight JVM / corrupt py4j state) and were the cause
    of the permanent wedge. The dead JVM is harmless; the startup orphan-reaper
    cleans it on the next server start.
    """
    global _ready, _error, _plugin_version, _thread

    # Single-flight guard: if MEBatch is already (re)initializing, don't kick
    # another reset — that would race two relaunches.
    with _lock:
        if not _ready and _thread.is_alive():
            log.info("reset() skipped — reinitialization already in progress")
            return
        _ready = False
        _plugin_version = None
        _error = "Restarting SNAP connection after gateway error..."

    log.warning("SNAP connection broken — relaunching MEBatch JVM in-process")

    # Reset SNAP's model-editor singleton so the next find_plugin re-activates
    # it (relaunches MEBatch). shutdown() sets is_active() False even if the
    # gateway is dead (the process field is cleared regardless).
    try:
        import snap.model_editor as _me
        _me.__MODEL_EDITOR__.shutdown()
    except Exception as exc:
        log.warning("model-editor shutdown during reset failed (continuing): %s", exc)

    # Force-kill the OLD (broken) MEBatch JVM ONCE, here, before relaunching.
    # When the gateway breaks the old JVM often lingers (gateway.shutdown() above
    # can't reach it), and a leftover live JVM blocks the relaunch from binding.
    # This runs BEFORE the _start thread launches the NEW JVM, so it never kills
    # the in-flight relaunch — that distinction (kill old once here, never in the
    # retry loop) is what makes recovery work.
    _kill_own_mebatch()

    # Drop the in-memory model cache — Java model objects are dead after the JVM
    # restart. get_model() lazily reloads each model from its autosaved .med on
    # next use, so an agent's model_id keeps working across a recovery.
    try:
        import snap_trace.session as _sess
        _sess._models.clear()
        log.info("Cleared in-memory model cache; models reload from .med on demand")
    except Exception:
        pass

    _error = None
    _thread = threading.Thread(target=_start, daemon=True, name="snap-reset")
    _thread.start()
    log.info("SNAP reset thread started — waiting for MEBatch to relaunch")
