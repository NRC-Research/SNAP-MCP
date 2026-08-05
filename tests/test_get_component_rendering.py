"""Validation for get_component's property rendering.

get_component summarizes a component by walking every public attribute and
calling str() on it. That is harmless on a PIPE and pathological on a VESSEL:
str() on a 3-D property table materializes the whole table, and the call did
not return at all on a plant-sized model (measured: >420 s, versus ~1 s for
every other metadata tool).

_render_prop describes bulk values instead of expanding them. These checks run
without SNAP -- they use stand-ins that fail loudly if the renderer touches
something it should not.

    python tests/test_get_component_rendering.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from snap_trace.tools.component_tools import _render_prop  # noqa: E402

failures = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}")
    if not ok:
        print(f"        want {want!r}")
        failures.append(label)


def contains(label, got, needle):
    ok = isinstance(got, str) and needle in got
    print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got!r}")
    if not ok:
        failures.append(label)


class ExplodingTable:
    """Stands in for Hydro3DPropertyTable.

    Its __len__ and __iter__ build the entire table in the real class, so the
    renderer must never call them. Here they raise instead, turning a
    regression into a test failure rather than a silent 10-minute call.
    """

    def __init__(self, rows=33, cols=24):
        self.row_count = rows
        self.column_count = cols

    def __len__(self):
        raise AssertionError("__len__ called on a table-like value "
                             "(this materializes the whole table)")

    def __iter__(self):
        raise AssertionError("__iter__ called on a table-like value")

    def __str__(self):
        raise AssertionError("__str__ called on a table-like value")


class Wrapper:
    """A cheap scalar-like SNAP wrapper (Length, Angle, CReal)."""

    def __init__(self, text):
        self._text = text

    def __str__(self):
        return self._text


class Unprintable:
    def __str__(self):
        raise RuntimeError("boom")


def main():
    print("\n-- scalars pass straight through")
    check("int", _render_prop(42), 42)
    check("float", _render_prop(1.5), 1.5)
    check("bool", _render_prop(True), True)
    check("None", _render_prop(None), None)
    check("short str", _render_prop("abc"), "abc")

    print("\n-- long strings are truncated, with the original length reported")
    out = _render_prop("x" * 900)
    ok = out.startswith("x" * 400) and "900 chars" in out and len(out) < 500
    print(f"  {'PASS' if ok else 'FAIL'}  long str truncated: ...{out[-40:]!r}")
    if not ok:
        failures.append("long str truncated")

    print("\n-- table-like values are described, never expanded")
    # The stand-in raises on __len__/__iter__/__str__, so this passing proves
    # the renderer used row_count/column_count only.
    out = _render_prop(ExplodingTable(33, 24))
    contains("shape reported", out, "33x24")
    contains("names the type", out, "ExplodingTable")
    contains("points at the right tool", out, "get_vessel_tables")

    print("\n-- table with unreadable shape still degrades safely")

    class BadShape:
        """Table-like, but the shape query itself fails."""

        @property
        def row_count(self):
            raise RuntimeError("nope")

        def __len__(self):
            raise AssertionError("__len__ called on a table-like value")

        def __str__(self):
            raise AssertionError("__str__ called on a table-like value")

    out = _render_prop(BadShape())
    contains("unknown shape handled", out, "not expanded")

    print("\n-- sized collections are described, not expanded")
    out = _render_prop(list(range(5000)))
    contains("list length reported", out, "5000 items")
    ok = "0, 1, 2" not in out
    print(f"  {'PASS' if ok else 'FAIL'}  list contents not expanded")
    if not ok:
        failures.append("list contents not expanded")

    print("\n-- scalar-like wrappers are expanded (they are cheap)")
    check("wrapper str", _render_prop(Wrapper("1.524 m")), "1.524 m")

    print("\n-- a raising __str__ does not break the whole summary")
    contains("str() failure contained", _render_prop(Unprintable()), "RuntimeError")

    print()
    if failures:
        print(f"FAILED ({len(failures)}): {', '.join(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
