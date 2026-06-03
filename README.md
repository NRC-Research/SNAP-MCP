# SNAP-MCP

A monorepo containing [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers that wrap the Symbolic Nuclear Analysis Program (SNAP) Python APIs as AI-callable tools. 

Using these servers, AI assistants (like Claude Code, Claude Desktop, GitHub Copilot, or autonomous agents like `crush`) can create, modify, inspect, validate, and export safety analysis input decks through natural language and self-correcting validation loops.

---

## IMPORTANT: Licensing Notice
All MCP servers in this repository interface with SNAP Python APIs and require a valid, licensed installation of **SNAP (Symbolic Nuclear Analysis Program)** and the corresponding code plug-ins to function.

If you or your organization do not have a license for SNAP, contact **Information Systems Laboratories (ISL), Inc.** to obtain one:
* **SNAP License Info**: [ISL Inc. SNAP Info](https://www.islinc.com/products/snapinfo)

---

## Exposed MCP Servers

This repository contains three separate MCP servers, each wrapping a different SNAP plug-in:

### 1. `snap-trace` (TRACE MCP)
- **Status**: Production-ready.
- **Location**: Root directory (`/`). Core logic resides in `snap_trace/` package. Entry point is `mcp_server.py`.
- **Purpose**: Build, inspect, and export TRACE thermal-hydraulic models.
- **Documentation**: See [snap_trace/README.md](./snap_trace/README.md).

### 2. `snap-relap` (RELAP5 MCP)
- **Status**: Production-ready. Includes autonomous error-correction helper signatures.
- **Location**: Subdirectory `snap-relap/`. Core logic is in the `snap_relap` package. Entry point is `snap-relap/mcp_server.py`.
- **Purpose**: Build, validate, and export RELAP5 models.
- **Documentation**: See [snap-relap/README.md](./snap-relap/README.md).

### 3. `snap-melcor` (MELCOR MCP)
- **Status**: In development. Python wrappers auto-generated from Java source; stubs implemented.
- **Location**: Subdirectory `snap-melcor/`. Core logic is in `snap-melcor` package. Entry point is `snap-melcor/mcp_server.py`.
- **Purpose**: Inspect and modify MELCOR2X models.
- **Documentation**: See [snap-melcor/README.md](./snap-melcor/README.md).

---

## Installation & Setup

To use any of the MCP servers, you must first install the package dependencies. It is recommended to use the editable mode so changes to the server logic are picked up immediately.

```bash
# 1. Clone the repository
git clone https://github.com/NRC-Research/SNAP-MCP.git
cd SNAP-MCP

# 2. Install base dependencies
pip install -e .

# 3. Install sub-project dependencies
pip install -e snap-relap/
pip install -e snap-melcor/
```

---

## Client Registration Examples

All three servers run as stdio subprocesses and can be registered with any standard MCP host. Replace `/path/to/snap/python` and `/path/to/SNAP-MCP` with your actual system paths.

### 1. Claude Code
Register the servers using the `claude mcp add` CLI command:

```bash
# Register snap-trace
claude mcp add snap-trace \
  -e SNAP_PYTHON_PATH=/path/to/snap/python \
  -- python /path/to/SNAP-MCP/mcp_server.py

# Register snap-relap
claude mcp add snap-relap \
  -e SNAP_PYTHON_PATH=/path/to/snap/python \
  -- python /path/to/SNAP-MCP/snap-relap/mcp_server.py
```

### 2. Claude Desktop
Add the servers under `mcpServers` in your configuration file (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "snap-trace": {
      "command": "python3",
      "args": ["/path/to/SNAP-MCP/mcp_server.py"],
      "env": {
        "SNAP_PYTHON_PATH": "/path/to/snap/python"
      }
    },
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

### 3. IDEs and Other Agentic Runners (e.g. `crush`)
To hook the servers into other environments (like Copilot CLI or headless agent platforms), define them in your environment's MCP configuration under the `"mcp"` key.

---

## Repository Documentation Guides
- **Developer Guide**: See `CODE_GUIDE.md` for architectural design, Py4J gateway setup, testing suites, and instructions for extending tools and components.
- **User Guide**: See `USER_GUIDE.md` for conversational examples, tips on unit conversion, component numbering schemas, and best practices.
