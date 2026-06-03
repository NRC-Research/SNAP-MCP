"""Model registry: in-memory TraceModel objects + SQLite persistence.

Every mutating operation should call autosave(model_id) so that models
survive MCP server restarts.
"""
from __future__ import annotations
import os
import sqlite3
import uuid
from pathlib import Path

import snap_trace.snap_env  # noqa: F401 — ensure SNAP path is on sys.path first

_WORKDIR = Path(os.environ.get("SNAP_TRACE_WORKDIR",
                               str(Path.home() / ".snap_trace" / "models")))
_DB_PATH = os.environ.get("SNAP_TRACE_DB",
                           str(Path.home() / ".snap_trace" / "models.db"))

_models: dict = {}


def _trace():
    """Lazy import of snap.codes.trace — re-resolved after each gateway reset."""
    import snap.codes.trace as _t
    return _t
_db: sqlite3.Connection | None = None


def _db_conn() -> sqlite3.Connection:
    global _db
    if _db is None:
        _WORKDIR.mkdir(parents=True, exist_ok=True)
        Path(_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        _db = sqlite3.connect(_DB_PATH, check_same_thread=False)
        _db.execute("""
            CREATE TABLE IF NOT EXISTS models (
                id       TEXT PRIMARY KEY,
                name     TEXT NOT NULL,
                med_path TEXT NOT NULL,
                version  TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        _db.commit()
    return _db


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


def _med_path(model_id: str) -> Path:
    return _WORKDIR / f"{model_id}.med"


# ── public API ────────────────────────────────────────────────────────────────

def create_model(name: str, version: str = "V5.0p9") -> tuple:
    model_id = _new_id()
    model = _trace().new_model(version)
    path = _med_path(model_id)
    model.save(str(path))
    _db_conn().execute(
        "INSERT INTO models (id, name, med_path, version) VALUES (?, ?, ?, ?)",
        (model_id, name, str(path), version),
    )
    _db_conn().commit()
    _models[model_id] = model
    return model_id, model


def register_model(name: str, model,
                   source_path: str) -> tuple:
    """Register an already-opened model (from open_med or import_ascii)."""
    model_id = _new_id()
    dest = _med_path(model_id)
    model.save(str(dest))
    _db_conn().execute(
        "INSERT INTO models (id, name, med_path, version) VALUES (?, ?, ?, ?)",
        (model_id, name, str(dest), None),
    )
    _db_conn().commit()
    _models[model_id] = model
    return model_id, model


def get_model(model_id: str):
    if model_id in _models:
        return _models[model_id]
    row = _db_conn().execute(
        "SELECT med_path FROM models WHERE id = ?", (model_id,)
    ).fetchone()
    if not row:
        raise ValueError(f"Unknown model_id '{model_id}'. Call list_models() to see available models.")
    model = _trace().open_model(row[0])
    _models[model_id] = model
    return model


def autosave(model_id: str) -> None:
    """Persist the current model state to its .med file."""
    if model_id in _models:
        row = _db_conn().execute(
            "SELECT med_path FROM models WHERE id = ?", (model_id,)
        ).fetchone()
        if row:
            _models[model_id].save(row[0])


def list_models() -> list[dict]:
    rows = _db_conn().execute(
        "SELECT id, name, version, created_at FROM models ORDER BY created_at DESC"
    ).fetchall()
    return [
        {"model_id": r[0], "name": r[1], "version": r[2], "created_at": r[3]}
        for r in rows
    ]
