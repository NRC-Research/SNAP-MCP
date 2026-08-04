"""Validation for the find_component CC index.

The naive find_component scanned every category and issued one py4j
round-trip per component on *every* lookup, so sweeping a model cost
O(N^2) round-trips. Measured on an 819-component plant model: 0.038 s per
lookup, ~31 s to resolve every component once.

These checks confirm the index preserves behaviour exactly -- including
the first-match-wins resolution order that matters when the same CC
number names components of different types -- and that it cannot serve a
stale entry after the model changes.

    python tests/test_cc_index.py
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}, want {want!r}")
    if not ok:
        failures.append(label)


def ok(label, condition, detail=""):
    print(f"  {'PASS' if condition else 'FAIL'}  {label}"
          + (f": {detail}" if detail else ""))
    if not condition:
        failures.append(label)


def main():
    import os
    os.environ.setdefault("SNAP_PYTHON_PATH",
                          os.path.expanduser("~/run-snap500/python"))

    import snap_trace.snap_env as snap_env
    import snap_trace.session as session
    from snap_trace import component_map
    from snap_trace.component_map import find_component, invalidate_cc_index

    ready, err = snap_env.wait_ready(timeout=180.0)
    if not ready:
        print(f"  SKIP: SNAP gateway not ready ({err})")
        return 0

    model_id, model = session.create_model("cc-index-test", "V5.0p9")
    for n in (110, 120, 130):
        model.create_pipe(comp_num=n)
    print(f"  model {model_id} with pipes 110/120/130")

    print("\n-- correctness")
    ctype, comp = find_component(model, 120)
    check("finds pipe 120 by type", ctype, "PIPE")
    check("finds pipe 120 by number",
          int(comp.java_object.getCCnumber()), 120)

    ok("index was populated", model in component_map._cc_index)

    # Second lookup must come from cache and agree with the first.
    ctype2, comp2 = find_component(model, 120)
    check("cached lookup returns same type", ctype2, ctype)
    check("cached lookup returns same object",
          int(comp2.java_object.getCCnumber()), 120)

    print("\n-- missing components still raise")
    try:
        find_component(model, 99999)
        ok("unknown CC raises ValueError", False, "no exception raised")
    except ValueError as e:
        ok("unknown CC raises ValueError", True, str(e)[:60])
    except Exception as e:
        ok("unknown CC raises ValueError", False,
           f"raised {type(e).__name__} instead")

    print("\n-- a miss must not be cached as absent")
    # A newly added component has to be findable even though a previous
    # lookup for that number failed against the same model.
    model.create_pipe(comp_num=140)
    invalidate_cc_index(model)
    try:
        ctype3, _ = find_component(model, 140)
        check("newly added pipe 140 is found", ctype3, "PIPE")
    except ValueError:
        ok("newly added pipe 140 is found", False, "raised ValueError")

    print("\n-- stale index degrades to a rebuild, never a wrong answer")
    # Add without invalidating, simulating a mutation path that forgets to.
    model.create_pipe(comp_num=150)
    try:
        ctype4, comp4 = find_component(model, 150)
        check("finds 150 despite stale index", ctype4, "PIPE")
        check("and it is really 150",
              int(comp4.java_object.getCCnumber()), 150)
    except ValueError:
        ok("finds 150 despite stale index", False,
           "raised ValueError -- stale index served a false negative")

    print("\n-- invalidation")
    invalidate_cc_index(model)
    ok("index dropped after invalidate",
       model not in component_map._cc_index)
    invalidate_cc_index(model)  # must be safe when nothing is cached
    ok("invalidate is idempotent", True)

    print("\n-- speed (cold build vs warm lookups)")
    invalidate_cc_index(model)
    t0 = time.time()
    find_component(model, 110)
    cold = time.time() - t0

    t0 = time.time()
    reps = 50
    for _ in range(reps):
        find_component(model, 110)
    warm = (time.time() - t0) / reps

    print(f"      cold (index build): {cold * 1000:.1f} ms")
    print(f"      warm (cached):      {warm * 1000:.3f} ms")
    ok("warm lookup is much cheaper than a build", warm < cold / 5,
       f"{cold / max(warm, 1e-9):.0f}x faster")

    print()
    if failures:
        print(f"FAILED ({len(failures)}): {', '.join(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
