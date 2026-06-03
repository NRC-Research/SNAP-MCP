"""MelgenModel session registry.

Holds open MelgenModel instances keyed by a short model_id string.
Mirrors snap_trace/session.py.

INVESTIGATE before implementing get_component / set_component_property:
  - Does MelgenModel.components() exist (inherited from MEDModel)?
  - What type do component objects have? What attributes?
  - Is set_property available, or is mutation export-only?
  See README.md § "What needs investigation".
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # snap.codes.melcor.MelgenModel imported lazily to avoid early init

_sessions: dict[str, object] = {}   # model_id -> MelgenModel
_next_id: int = 1


def _new_id() -> str:
    global _next_id
    mid = f"melcor_{_next_id}"
    _next_id += 1
    return mid


def register(model_id: str, model) -> None:
    """Store a MelgenModel under the given model_id."""
    _sessions[model_id] = model


def get(model_id: str):
    """Return the MelgenModel for model_id, or raise KeyError."""
    if model_id not in _sessions:
        raise KeyError(f"No MELCOR model session '{model_id}'. "
                       "Use import_melgen or open_med_model first.")
    return _sessions[model_id]


def remove(model_id: str) -> None:
    """Close and remove a session."""
    model = _sessions.pop(model_id, None)
    if model is not None:
        try:
            model.close()
        except Exception:
            pass


def list_ids() -> list[str]:
    return list(_sessions.keys())
