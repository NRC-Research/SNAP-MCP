"""Validation for the derived GRAV term and the get_model_options tool.

Covers the two gaps that made it impossible to reason about a vessel
junction's gravity term through the MCP:

  * GRAV was not reported at all, and is not reachable through SNAP's Python
    binding (no edge.grav / edge.getGrav()) -- it has to be derived as
    sin(angle).
  * The edge inclination was documented as degrees but is radians, so a
    vertical edge (pi/2) read as "1.57 degrees", i.e. nearly horizontal.
  * IELV was unreachable, so nothing could tell whether GRAV is editable.

The pure-function checks run anywhere.  The live checks need a working SNAP
gateway and are skipped with a clear message when one is not available.

    python tests/test_grav_and_model_options.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from snap_trace.tools.component_tools import _deg, _grav_from_angle  # noqa: E402

failures = []


def check(label, got, want, tol=1e-12):
    ok = (got == want) if not isinstance(want, float) else abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def check_is(label, got, want):
    ok = got is want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def test_pure():
    print("\n-- derived GRAV / angle conversion (no SNAP needed)")

    # The relationship the plug-in defines: getGrav() == sin(edgeAngle).
    check("horizontal edge -> grav 0", _grav_from_angle(0.0), 0.0)
    check("vertical up (pi/2) -> grav +1", _grav_from_angle(math.pi / 2), 1.0)
    check("vertical down (-pi/2) -> grav -1", _grav_from_angle(-math.pi / 2), -1.0)
    check("45 deg -> grav sin(45)", _grav_from_angle(math.pi / 4),
          math.sin(math.pi / 4))

    # Round-trip against setGrav's asin(), which is how a written value lands.
    for g in (0.0, 0.25, -0.5, 1.0, -1.0):
        check(f"round-trip grav {g}", _grav_from_angle(math.asin(g)), g, tol=1e-12)

    print("\n-- radians vs degrees")
    check("pi/2 rad -> 90 deg", _deg(math.pi / 2), 90.0, tol=1e-9)
    check("0 rad -> 0 deg", _deg(0.0), 0.0)

    print("\n-- sentinels must pass through, never become plausible numbers")
    # sin('unset') would be nonsense; a silent 0.0 would read as "horizontal".
    check("grav of 'unset' stays 'unset'", _grav_from_angle("unset"), "unset")
    check("deg of 'unset' stays 'unset'", _deg("unset"), "unset")
    check_is("grav of None stays None", _grav_from_angle(None), None)
    check_is("deg of None stays None", _deg(None), None)
    # bool is an int subclass; must not be treated as an angle.
    check_is("grav of True stays True", _grav_from_angle(True), True)


def test_live():
    print("\n-- live SNAP checks")
    try:
        import snap_trace.snap_env as snap_env
        import snap_trace.session as session
        from snap_trace.component_map import find_component
    except Exception as e:
        print(f"  SKIP: cannot import SNAP layer ({e})")
        return

    ok, err = snap_env.wait_ready(timeout=180.0)
    if not ok:
        print(f"  SKIP: SNAP gateway not ready ({err})")
        return

    model_id, model = session.create_model("grav-test", "V5.0p9")
    print(f"  created model {model_id}")

    # create_pipe(initializer, comp_num) -- passing the number positionally
    # would be read as the initializer, so name it. Default geometry is fine;
    # only the presence of an edge table matters here.
    pipe = model.create_pipe(comp_num=110)
    edges = getattr(pipe, "edges", None)
    if not edges:
        print("  FAIL: pipe has no edge table")
        failures.append("live: pipe edges")
        return

    edge = edges[0]

    # The binding genuinely does not expose GRAV -- if this ever starts
    # working, prefer the native getter over our derivation.
    exposed = [n for n in dir(edge) if "grav" in n.lower()]
    check("binding still hides GRAV (derivation required)", exposed, [])

    angle = float(edge.angle)
    check("derived grav matches sin(angle)", _grav_from_angle(angle),
          math.sin(angle))

    # IELV must be readable, and a fresh model sits at the TRACE default of 0.
    namelist = model.model_options().namelist
    check("default model reports ielv 0", int(namelist.ielv.value), 0)

    from snap_trace.tools.model_tools import _namelist_value
    check("ielv unwraps to an int", _namelist_value(namelist.ielv), 0)

    nvgrav = _namelist_value(namelist.nvgrav)
    ok_nvgrav = isinstance(nvgrav, (int, str, dict))
    print(f"  {'PASS' if ok_nvgrav else 'FAIL'}  nvgrav enum unwraps to a "
          f"JSON-safe value: {nvgrav!r}")
    if not ok_nvgrav:
        failures.append("nvgrav unwrap")

    import json
    try:
        json.dumps({"nvgrav": nvgrav, "ielv": _namelist_value(namelist.ielv)})
        print("  PASS  unwrapped options are JSON-serializable")
    except TypeError as e:
        print(f"  FAIL  options not JSON-serializable: {e}")
        failures.append("json serializable")


def main():
    test_pure()
    test_live()
    print()
    if failures:
        print(f"FAILED ({len(failures)}): {', '.join(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
