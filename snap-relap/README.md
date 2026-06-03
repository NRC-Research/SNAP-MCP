# snap-relap

A companion Model Context Protocol (MCP) server for **RELAP5** input deck inspection and modification. It wraps the SNAP RELAP5 Python bindings (`snap.codes.relap`) as AI-callable tools, allowing an AI assistant to build, edit, validate, and export RELAP5 models.

---

## IMPORTANT: Licensing Notice
These MCP servers use **SNAP (Symbolic Nuclear Analysis Program)** as their backend. In order to run the server, you must have a licensed installation of SNAP and the RELAP5 plug-in. 

If you or your organization do not have a license for SNAP, please contact **Information Systems Laboratories (ISL), Inc.** to obtain one:
* **SNAP License Info**: [ISL Inc. SNAP Info](https://www.islinc.com/products/snapinfo)

---

## Prerequisites
- A licensed installation of SNAP with the RELAP5 plug-in.
- Python 3.8+
- Py4J and anyio/fastmcp dependencies (installed automatically via `pip`).

---

## Installation

```bash
cd snap-relap
pip install -e .
```

---

## Registering with Agentic Clients

Since this server uses stdio to communicate with clients, it can be registered with any MCP-capable agentic host. Replace `/path/to/snap/python` and `/path/to/SNAP-MCP` with your actual system paths.

### 1. Claude Code
Run the following command in your terminal to register the server with Claude Code:
```bash
claude mcp add snap-relap \
  -e SNAP_PYTHON_PATH=/path/to/snap/python \
  -- python3 /path/to/SNAP-MCP/snap-relap/mcp_server.py
```

### 2. Claude Desktop
Add the following entry under `mcpServers` in your Claude Desktop configuration file (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "snap-relap": {
      "command": "python3",
      "args": ["/path/to/SNAP-MCP/snap-relap/mcp_server.py"],
      "env": {
        "SNAP_PYTHON_PATH": "/path/to/snap/python"
      }
    }
  }
}
```

### 3. GitHub Copilot CLI / VS Code Copilot
For Copilot or general MCP-compatible IDE extensions, add the following to your MCP configuration file:
```json
{
  "mcp": {
    "snap-relap": {
      "command": "python3",
      "args": ["/path/to/SNAP-MCP/snap-relap/mcp_server.py"],
      "env": {
        "SNAP_PYTHON_PATH": "/path/to/snap/python"
      }
    }
  }
}
```

### 4. Autonomous Runners (e.g., `crush`)
To register the server for headless execution with autonomous agent harnesses like `crush`, configure the server under the top-level `"mcp"` key of the runner config (e.g., `~/.config/crush/crush.json`).

---

## Autonomous Self-Correction Loop

This MCP is designed to support fully autonomous model-building loops for AI agents. 

When an AI agent builds a model from a high-level (and potentially incomplete) user prompt, certain tool-specific configurations (like simulation time-step tables or boundary volume dimensions) may be omitted. To resolve this:

1. The validation tool (`validate_model`) runs both SNAP's built-in Java validation and Python-level checks.
2. If any constraint is violated, the validator returns an enriched error string containing an explicit, copy-pasteable fix signature, e.g.:
   > `Error: Model Options: Time Step cards have not been defined. [Fix: Use set_model_options(model_id, 'timestep_table', [[100.0, 1e-6, 0.01, 3, 100, 1000, 1000]]) to define the transient time steps.]`
3. The AI agent parses the error, identifies the `[Fix: ...]` instruction, invokes the specified tool, and successfully corrects the model without human intervention.

---

## Tools Exposed

| Tool | Parameters | Description |
|------|------------|-------------|
| `relap_status` | None | Check if the RELAP5 plugin is loaded. |
| `create_model` | `name` (str), `version` (str) | Start a new RELAP5 model session (default version: `MOD3.3`). |
| `import_relap` | `model_id` (str), `path` (str) | Import a RELAP5 ASCII input deck. |
| `open_med_model` | `path` (str) | Open an existing `.med` model file. |
| `list_models` | None | List all open model sessions. |
| `close_model` | `model_id` (str) | Close a model session. |
| `get_component_schema` | `type` (str) | Describe a component type's properties and guidance. |
| `add_component` | `model_id` (str), `type` (str), `cc` (int), `properties` (dict) | Add a new component to the model. |
| `set_component_property` | `model_id` (str), `cc` (int), `name` (str), `value` (any) | Set a property on an existing component (supports list broadcasting). |
| `set_model_options` | `model_id` (str), `name` (str), `value` (any) | Set model-level options (e.g. `timestep_table`). |
| `list_components` | `model_id` (str) | List all components in a model. |
| `get_component` | `model_id` (str), `cc` (int) | Inspect all readable properties of one component. |
| `connect_components` | `model_id` (str), `source_cc` (int), `target_cc` (int), `source_slot` (str), `target_slot` (str) | Wire a hydraulic junction between components. |
| `get_connections` | `model_id` (str) | Show all junction connections in the model. |
| `validate_model` | `model_id` (str) | Run built-in validation checks (errors and warnings). |
| `review_model` | `model_id` (str) | Audit a model: component inventory, connections, and validation issues. |
| `export_relap` | `model_id` (str), `path` (str), `force` (bool) | Export the model to a RELAP5 ASCII deck (`.inp`). |
| `save_med` | `model_id` (str), `path` (str) | Save the model as a SNAP `.med` file. |
