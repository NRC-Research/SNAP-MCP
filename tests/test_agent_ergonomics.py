"""Validation for the changes that let a weak agent actually drive this server.

Three defects made the tool surface unusable from crush/devstral even though
every tool worked correctly when driven by hand:

  * A gateway-touching tool called before MEBatch finished starting was
    refused with "call snap_status() and wait until ready=true before
    retrying". An LLM agent has no clock and no sleep tool, so it cannot obey
    that: it spends its whole turn budget re-polling snap_status and returns
    nothing. Note the tools already called wait_ready() internally -- the
    wrapper raised before the body ever ran, so the two mechanisms fought.
  * Callers reliably guess 'path' for open_med_model/import_trcin, whose
    parameters are 'med_file_path'/'trcin_path'. The resulting validation
    error names a field the caller never used, so it reads as a broken tool
    and the agent retries the identical call.
  * The server instructions wrote tool names bare ("create_model()"), but MCP
    clients expose them prefixed ("mcp_snap_trace_create_model"), which primed
    the model to emit a name that does not exist.

The _resolve_path checks run anywhere. The wrapper check imports mcp_server,
which starts MEBatch, so it runs only with SNAP_MCP_LIVE=1.

    python tests/test_agent_ergonomics.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# snap_env refuses to import without SNAP_PYTHON_PATH. The pure checks below
# never reach SNAP, so point it at an empty directory when it is unset; the
# background init thread fails harmlessly and status() reports the error.
os.environ.setdefault("SNAP_PYTHON_PATH", tempfile.mkdtemp(prefix="snapmcp-test-"))

from snap_trace.tools.model_tools import _resolve_path  # noqa: E402

failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def check_raises(label, fn, needle):
    try:
        fn()
    except ValueError as exc:
        ok = needle in str(exc)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}: {str(exc)[:70]!r}")
        if not ok:
            failures.append(label)
    except Exception as exc:  # wrong exception type is still a failure
        print(f"  FAIL  {label}: raised {type(exc).__name__}, want ValueError")
        failures.append(label)
    else:
        print(f"  FAIL  {label}: did not raise")
        failures.append(label)


def test_resolve_path():
    print("\n-- path alias resolution (no SNAP needed)")
    P = "/models/plant.med"
    Q = "/models/other.med"

    check("canonical only",
          _resolve_path("open_med_model", "med_file_path", P, ""), P)
    check("alias only",
          _resolve_path("open_med_model", "med_file_path", "", P), P)
    check("both, identical",
          _resolve_path("open_med_model", "med_file_path", P, P), P)

    # Whitespace-only is not a path; it must fall through to the alias rather
    # than silently winning and handing SNAP a blank filename.
    check("blank canonical falls through to alias",
          _resolve_path("open_med_model", "med_file_path", "   ", P), P)
    check("surrounding whitespace stripped",
          _resolve_path("open_med_model", "med_file_path", f"  {P}  ", ""), P)

    # A real mistake must still be reported.
    check_raises("both given and different",
                 lambda: _resolve_path("open_med_model", "med_file_path", P, Q),
                 "both given but differ")
    check_raises("neither given",
                 lambda: _resolve_path("open_med_model", "med_file_path", "", ""),
                 "a file path is required")
    check_raises("error names the canonical parameter",
                 lambda: _resolve_path("import_trcin", "trcin_path", "", ""),
                 "trcin_path")


def test_wrapper_waits():
    """A tool called before ready must wait for MEBatch, not refuse."""
    print("\n-- wrapper waits for readiness instead of refusing")
    if os.environ.get("SNAP_MCP_LIVE") != "1":
        print("  SKIP  set SNAP_MCP_LIVE=1 to run (imports mcp_server, starts MEBatch)")
        return

    import mcp_server
    import snap_trace.snap_env as snap_env

    calls = {"wait": 0, "ran": 0}
    real_is_ready, real_wait_ready = snap_env.is_ready, snap_env.wait_ready

    def fake_is_ready():
        return False

    def fake_wait_ready(timeout=None):
        calls["wait"] += 1
        return True, None          # becomes ready while the call waits

    def tool():
        calls["ran"] += 1
        return "ok"

    snap_env.is_ready, snap_env.wait_ready = fake_is_ready, fake_wait_ready
    try:
        wrapped = mcp_server._make_reconnect_wrapper(tool, is_async=False)
        check("not-ready call still runs", wrapped(), "ok")
        check("waited exactly once", calls["wait"], 1)
        check("tool body executed", calls["ran"], 1)

        # A start that never completes must fail with actionable text, not hang.
        def never_ready(timeout=None):
            return False, "MEBatch exited during startup"

        snap_env.wait_ready = never_ready
        try:
            mcp_server._make_reconnect_wrapper(tool, is_async=False)()
        except RuntimeError as exc:
            msg = str(exc)
            check("failure says retrying will not help",
                  "retrying immediately will not help" in msg, True)
            check("failure surfaces the underlying detail",
                  "MEBatch exited during startup" in msg, True)
        else:
            print("  FAIL  stuck startup did not raise")
            failures.append("stuck startup did not raise")
    finally:
        snap_env.is_ready, snap_env.wait_ready = real_is_ready, real_wait_ready


if __name__ == "__main__":
    test_resolve_path()
    test_wrapper_waits()
    print(f"\n{len(failures)} failure(s)" + (f": {failures}" if failures else ""))
    sys.exit(1 if failures else 0)
