"""Validation for list_models' summary-first behaviour.

The model registry is append-only: one row per create_model / open_med_model /
import_trcin, never pruned, so it grows without bound (159 rows on the dev box
after a few weeks). list_models returned every row, and a prompt like "call
list_models and report exactly what it returns" then cost ~5 minutes -- the
rows re-enter the conversation as prompt and are regenerated token by token on
the way out. Measured on a self-hosted devstral: 15.9 KB of output took 332 s, while
the same question phrased as a count took 20 s.

    python tests/test_list_models_summary.py
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("SNAP_PYTHON_PATH", tempfile.mkdtemp(prefix="snapmcp-test-"))

import snap_trace.session as session  # noqa: E402
from snap_trace.tools import model_tools  # noqa: E402

failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


class FakeMCP:
    """Capture the registered tool functions without a live MCP server."""

    def __init__(self):
        self.tools = {}

    def tool(self, *a, **kw):
        def deco(fn):
            self.tools[fn.__name__] = fn
            return fn
        return deco

    def resource(self, *a, **kw):
        return lambda fn: fn


def build_list_models(rows):
    mcp = FakeMCP()
    real = session.list_models
    session.list_models = lambda: list(rows)
    try:
        model_tools.register(mcp)
    finally:
        session.list_models = real
    # Re-bind so the captured closure keeps using our stub.
    fn = mcp.tools["list_models"]
    session.list_models = lambda: list(rows)
    return fn


def rows_named(n, name="PLANT_LBLOCA_PK_SS"):
    return [{"model_id": f"{i:08x}", "name": f"{name}" if i % 2 else "other",
             "version": "V5.0p9", "created_at": f"2026-08-{(i % 28) + 1:02d}"}
            for i in range(n)]


def main():
    real = session.list_models
    try:
        print("\n-- default is bounded, and says so")
        rows = rows_named(159)
        fn = build_list_models(rows)

        r = fn()
        check("total reports every match", r["total"], 159)
        check("default returns 20", r["returned"], 20)
        check("models list length matches 'returned'", len(r["models"]), 20)
        check("note present when shortened", "note" in r, True)
        check("newest first preserved", r["models"][0], rows[0])

        print("\n-- limit and full")
        check("limit honoured", fn(limit=5)["returned"], 5)
        check("limit below 1 clamps to 1", fn(limit=0)["returned"], 1)
        check("detail='full' returns all", fn(detail="full")["returned"], 159)
        check("no note when nothing hidden", "note" in fn(detail="full"), False)

        print("\n-- name_contains filter")
        f = fn(name_contains="plant", detail="full")
        check("filter is case-insensitive", f["returned"], 79)
        check("total reflects the filter, not the registry", f["total"], 79)
        check("filter echoed back", f["name_contains"], "plant")
        check("non-matching filter is empty, not an error",
              fn(name_contains="nope")["total"], 0)

        print("\n-- small registry needs no truncation")
        fn_small = build_list_models(rows_named(3))
        r = fn_small()
        check("returns all when under limit", r["returned"], 3)
        check("no note when under limit", "note" in r, False)
    finally:
        session.list_models = real


if __name__ == "__main__":
    main()
    print(f"\n{len(failures)} failure(s)" + (f": {failures}" if failures else ""))
    sys.exit(1 if failures else 0)
