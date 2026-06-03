# snap-relap

A companion Model Context Protocol (MCP) server for **RELAP5** input deck inspection and modification. It wraps the SNAP RELAP5 Python bindings (`snap.codes.relap`) as AI-callable tools.

## Installation

```bash
cd snap-relap
pip install -e .
```

To register with Claude Code:
```bash
claude mcp add snap-relap \
  -e SNAP_PYTHON_PATH=/path/to/snap/python \
  -- python /path/to/SNAP-MCP/snap-relap/mcp_server.py
```

## Tools Exposed

- `relap_status`: Check if the RELAP5 plugin is loaded.
- `create_model`: Start a new RELAP5 model session (default version: `MOD3.3`).
- `import_relap`: Import a RELAP5 ASCII input deck.
- `open_med_model`: Open an existing `.med` model file.
- `list_models`: List all open model sessions.
- `close_model`: Close a model session.
- `validate_model`: Run built-in validation checks.
- `export_relap`: Export the model to a RELAP5 ASCII deck (`.inp`).
- `save_med`: Save the model to a `.med` file.
