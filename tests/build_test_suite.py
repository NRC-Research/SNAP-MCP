"""
Builds the SNAP-MCP test suite from the TRACE regression model master list.

Filters to passing models (empty <FailureMode />) in selected suites, picks
5 representative models per suite (preferring simpler ones — no SupportFiles),
and copies them (plus any needed support files) to tests/suite/.

Usage:
    python tests/build_test_suite.py
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

MASTERLIST = Path(
    os.environ.get(
        "TRACE_MASTERLIST",
        Path("~/TRACE-regression-models/MasterList").expanduser()
    )
)
SUPPORT_ROOT = MASTERLIST / "support_files"
SUITE_DIR = Path(__file__).parent / "suite"

TARGET_SUITES = ["Short", "Short2", "Valve", "Pump", "Tee", "Contan"]
MODELS_PER_SUITE = 5


def parse_header(text: str) -> dict:
    fm_empty = bool(
        re.search(r"<FailureMode\s*/>", text)
        or re.search(r"<FailureMode>\s*</FailureMode>", text)
    )
    suites_block = re.search(r"<Suites>(.*?)</Suites>", text, re.DOTALL)
    suites = []
    if suites_block:
        suites = [s.strip() for s in suites_block.group(1).strip().split() if s.strip()]
    support_block = re.search(r"<SupportFiles>(.*?)</SupportFiles>", text, re.DOTALL)
    support_files = []
    if support_block and support_block.group(1).strip():
        support_files = [s.strip() for s in support_block.group(1).strip().split() if s.strip()]
    purpose_m = re.search(r"<Purpose>(.*?)</Purpose>", text, re.DOTALL)
    purpose = purpose_m.group(1).strip() if purpose_m else ""
    return {
        "passing": fm_empty,
        "suites": suites,
        "support_files": support_files,
        "purpose": purpose,
    }


def find_support_file(name: str) -> Path | None:
    """Search support_files/ recursively for a file by name."""
    for p in SUPPORT_ROOT.rglob(name):
        return p
    return None


def build():
    SUITE_DIR.mkdir(parents=True, exist_ok=True)

    # Bucket all passing models by suite
    by_suite: dict[str, list[dict]] = {s: [] for s in TARGET_SUITES}

    for inp in sorted(MASTERLIST.glob("*.inp")):
        try:
            text = inp.read_text(errors="replace")[:3000]
        except Exception:
            continue
        meta = parse_header(text)
        if not meta["passing"]:
            continue
        for suite in meta["suites"]:
            if suite in by_suite:
                by_suite[suite].append({
                    "path": inp,
                    "support_files": meta["support_files"],
                    "purpose": meta["purpose"],
                    "suites": meta["suites"],
                })

    copied: list[dict] = []
    missing_support: list[str] = []

    for suite, candidates in by_suite.items():
        # Prefer models with no support files (simpler), then fall back to those with files
        no_support = [m for m in candidates if not m["support_files"]]
        with_support = [m for m in candidates if m["support_files"]]
        ordered = no_support + with_support
        selected = ordered[:MODELS_PER_SUITE]

        dest_dir = SUITE_DIR / suite
        dest_dir.mkdir(exist_ok=True)

        for model in selected:
            src = model["path"]
            dst = dest_dir / src.name
            shutil.copy2(src, dst)

            # Copy any support files alongside the model
            for sf in model["support_files"]:
                sfpath = find_support_file(sf)
                if sfpath:
                    shutil.copy2(sfpath, dest_dir / sfpath.name)
                else:
                    missing_support.append(f"{src.name}: {sf}")

            copied.append({
                "suite": suite,
                "file": src.name,
                "purpose": model["purpose"],
                "support_files": model["support_files"],
            })

    # Write manifest
    manifest_path = SUITE_DIR / "manifest.md"
    lines = ["# Test Suite Manifest\n\n"]
    lines.append(f"Total models: {len(copied)}\n\n")
    for suite in TARGET_SUITES:
        suite_models = [m for m in copied if m["suite"] == suite]
        lines.append(f"## {suite} ({len(suite_models)} models)\n\n")
        for m in suite_models:
            sf = f" _(support: {', '.join(m['support_files'])})_" if m["support_files"] else ""
            lines.append(f"- `{m['file']}`{sf}\n")
            if m["purpose"]:
                lines.append(f"  - {m['purpose']}\n")
        lines.append("\n")

    if missing_support:
        lines.append("## Missing support files\n\n")
        for ms in missing_support:
            lines.append(f"- {ms}\n")

    manifest_path.write_text("".join(lines))

    print(f"Copied {len(copied)} models to {SUITE_DIR}")
    for suite in TARGET_SUITES:
        n = sum(1 for m in copied if m["suite"] == suite)
        print(f"  {suite}: {n}")
    if missing_support:
        print(f"\nWARNING: {len(missing_support)} support files not found:")
        for ms in missing_support:
            print(f"  {ms}")
    print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    build()
