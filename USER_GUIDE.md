# SNAP-MCP User Guide

SNAP-MCP lets you build and inspect TRACE thermal-hydraulic models by talking to an AI assistant. You describe what you want; the assistant handles the SNAP API calls.

---

## Setup

### Register the server (one-time)

Run this from your terminal — it writes the registration to `~/.claude.json` so Claude Code picks it up automatically on every launch:

```bash
claude mcp add snap-trace \
  -e SNAP_PYTHON_PATH=/path/to/run-snap500/python \
  -e SNAP_TRACE_DB=~/.snap_trace/models.db \
  -e SNAP_TRACE_WORKDIR=~/.snap_trace/models \
  -- /usr/bin/python3 /path/to/SNAP-MCP/mcp_server.py
```

Replace `/path/to/run-snap500/python` with your actual SNAP installation path (e.g. `~/run-snap500/python`) and `/path/to/SNAP-MCP/mcp_server.py` with the full path to this repo's entry point.

Verify the server registered and is reachable:

```bash
claude mcp list
# snap-trace: /usr/bin/python3 ... - ✓ Connected
```

If you see `✓ Connected`, restart your Claude Code session — the `snap-trace` tools become available in new sessions after registration.

> **Note:** Do not add `mcpServers` to `~/.claude/settings.json` or `~/.claude/claude_code_config.json` — those files are not read for MCP server registration. `claude mcp add` (which writes to `~/.claude.json`) is the correct method.

### For Claude Desktop

Add the server under `mcpServers` in `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "snap-trace": {
      "command": "/usr/bin/python3",
      "args": ["/path/to/SNAP-MCP/mcp_server.py"],
      "env": {
        "SNAP_PYTHON_PATH": "/path/to/run-snap500/python",
        "SNAP_TRACE_DB": "/Users/you/.snap_trace/models.db",
        "SNAP_TRACE_WORKDIR": "/Users/you/.snap_trace/models"
      }
    }
  }
}
```

### Confirm it's working

Once registered, ask your assistant:

> "Check the SNAP connection status."

The assistant will call `snap_status()` and tell you whether SNAP is ready. If it says "initializing", wait about 15–30 seconds and ask again — MEBatch starts in the background when the server launches.

---

## Opening and inspecting an existing model

> "Using the snap-mcp tools, load the model at `/Users/me/models/test.med` and give me a brief summary."

The assistant will open the file, list all components, and describe the model — component types, counts, and any notable configuration it can read.

> "What components are in the model? List them by type."

> "Show me the properties on pipe 21."

> "What is the hydraulic topology — how are the components connected?"

> "What are the initial conditions on pipe 21?"

---

## Importing a TRACE ASCII input deck

> "Import the file `/Users/me/runs/reactor.inp` and tell me what's in it."

> "Load that .inp file and check whether it passes SNAP's validation."

---

## Building a model from scratch

Just describe what you want. The assistant knows the TRACE component types, their required properties, and how to connect them.

> "Create a new TRACE model called 'Simple Loop' with a fill, a 20-cell pipe, and a break. Connect them in series and set reasonable initial conditions."

> "Add a cylindrical heat structure with 9 radial nodes coupled to pipe 21."

> "Add a signal variable that monitors the liquid temperature at the outlet of pipe 21."

> "Add a PID control block with a gain of 2.0."

For more complex models you can build incrementally:

> "Start with a FILL at 6 bar and 420 K."  
> "Now add a 4-meter pipe with 20 cells and 0.3 m hydraulic diameter."  
> "Connect them."  
> "Add a BREAK at 40 bar."  
> "Validate the model."

---

## Validating and exporting

> "Validate the model and tell me if there are any errors."

> "Export the model to `/Users/me/runs/output.inp`."

> "Save a .med copy to `/Users/me/models/my_model.med`."

> "Export the model and show me the first 50 lines of the TRCIN file."

---

## Resuming work across sessions

Models are saved automatically after every change. If you close and reopen your AI client:

> "List the models I've created previously."

> "Resume work on the model called 'Simple Loop'."

---

## Tips

- **Be specific about units.** SNAP uses SI by default (Pa, K, m, kg/s). Tell the assistant if you want to work in other units.
- **Component numbers matter.** TRACE uses integer CC numbers to identify components. If you have a preference (e.g. pipes in the 20s, breaks in the 10s), say so.
- **You can ask the assistant to explain.** "Why does a FILL need an ifty parameter?" works — the assistant has access to SNAP's component documentation.
- **Iteration is fine.** Add components one at a time, inspect after each step, and correct as you go.
