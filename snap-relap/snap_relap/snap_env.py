"""SNAP environment initialisation for the RELAP plugin.

Mirrors snap_trace/snap_env.py. The SNAP Python path must be on sys.path
before any snap.codes.relap import is attempted.
"""

import os
import sys


def init_snap_env() -> None:
    """Add the SNAP Python directory to sys.path if not already present.

    Reads SNAP_PYTHON_PATH from the environment.
    Falls back to the standard AMI install locations.
    """
    snap_python_path = os.environ.get("SNAP_PYTHON_PATH")

    if not snap_python_path:
        # Standard install locations
        candidates = [
            os.path.expanduser("~/snap/python"),         # user-local RHEL install
            "/opt/snap/python",                          # system RHEL9 install
            r"C:\Program Files\snap\python",             # Windows
            os.path.expanduser("~/run-snap500/python"),  # local development
        ]
        for candidate in candidates:
            if os.path.isdir(candidate):
                snap_python_path = candidate
                break

    if not snap_python_path:
        sys.stderr.write(
            "snap-relap: SNAP Python path not found. "
            "Set SNAP_PYTHON_PATH environment variable.\n"
        )
        return

    if snap_python_path not in sys.path:
        sys.path.insert(0, snap_python_path)

    # Verify the RELAP plugin is importable.
    # Save and restore the real sys.stdout around the import.
    _real_stdout = sys.stdout
    try:
        import snap.codes.relap  # noqa: F401
    except ImportError as exc:
        sys.stderr.write(
            f"snap-relap: could not import snap.codes.relap: {exc}\n"
            "Ensure the RELAP plugin jar is installed in SNAP's plugins/ directory.\n"
        )
    finally:
        sys.stdout = _real_stdout
