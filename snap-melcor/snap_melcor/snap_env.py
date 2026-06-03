"""SNAP environment initialisation for the MELCOR2X plugin.

Mirrors snap_trace/snap_env.py. The SNAP Python path must be on sys.path
before any snap.codes.melcor import is attempted.

INVESTIGATE: confirm the MELCOR2X plugin jar is present in the SNAP
plugins/ directory on RHEL9 AMIs (/opt/snap/plugins/melcor2x.jar) and
Windows AMIs (C:\\Program Files\\snap\\plugins\\melcor2x.jar).
"""

import os
import sys


def init_snap_env() -> None:
    """Add the SNAP Python directory to sys.path if not already present.

    Reads SNAP_PYTHON_PATH from the environment (set in crush.json env block).
    Falls back to the standard AMI install locations.
    """
    snap_python_path = os.environ.get("SNAP_PYTHON_PATH")

    if not snap_python_path:
        # Standard install locations
        candidates = [
            os.path.expanduser("~/snap/python"),         # user-local RHEL install
            "/opt/snap/python",                          # system RHEL9 install
            r"C:\Program Files\snap\python",             # Windows
        ]
        for candidate in candidates:
            if os.path.isdir(candidate):
                snap_python_path = candidate
                break

    if not snap_python_path:
        sys.stderr.write(
            "snap-melcor: SNAP Python path not found. "
            "Set SNAP_PYTHON_PATH in the crush.json env block.\n"
        )
        return

    if snap_python_path not in sys.path:
        sys.path.insert(0, snap_python_path)

    # Verify the MELCOR plugin is importable.
    # snap.codes.melcor replaces sys.stdout with a _StreamLogHandler object
    # that lacks a .buffer attribute, which breaks FastMCP's stdio transport.
    # Save and restore the real sys.stdout around the import so that the MCP
    # server can wrap sys.stdout.buffer after initialization completes.
    _real_stdout = sys.stdout
    try:
        import snap.codes.melcor  # noqa: F401
    except ImportError as exc:
        sys.stderr.write(
            f"snap-melcor: could not import snap.codes.melcor: {exc}\n"
            "Ensure the MELCOR2X plugin jar is installed in SNAP's plugins/ directory.\n"
        )
    finally:
        sys.stdout = _real_stdout
