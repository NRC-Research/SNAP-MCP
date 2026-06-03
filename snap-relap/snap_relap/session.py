"""RELAP model session registry.

Holds open RELAP model instances keyed by a short model_id string.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass  # snap.codes.relap.RelapModel imported lazily to avoid early init

_sessions: dict[str, object] = {}   # model_id -> RelapModel
_next_id: int = 1


def _new_id() -> str:
    global _next_id
    mid = f"relap_{_next_id}"
    _next_id += 1
    return mid


def register(model_id: str, model) -> None:
    """Store a RelapModel under the given model_id."""
    _sessions[model_id] = model


def get(model_id: str):
    """Return the RelapModel for model_id, or raise KeyError."""
    if model_id not in _sessions:
        raise KeyError(f"No RELAP model session '{model_id}'. "
                       "Use import_relap or open_med_model first.")
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
