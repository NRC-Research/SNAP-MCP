# snap-trace

A Model Context Protocol (MCP) server that exposes SNAP's **TRACE** Python API (`snap.codes.trace`) as AI-callable tools. An AI assistant (Claude Code, Claude Desktop, or any MCP-compatible client) can create, modify, validate, and export TRACE thermal-hydraulic input decks through natural conversation.

---

## IMPORTANT: Licensing Notice
This MCP server uses **SNAP (Symbolic Nuclear Analysis Program)** as its backend. In order to run the server, you must have a licensed installation of SNAP and the TRACE plug-in. 

If you or your organization do not have a license for SNAP, please contact **Information Systems Laboratories (ISL), Inc.** to obtain one:
* **SNAP License Info**: [ISL Inc. SNAP Info](https://www.islinc.com/products/snapinfo)

---

## Prerequisites
- A licensed installation of SNAP with the TRACE plug-in.
- Python 3.8+
- Py4J and anyio/fastmcp dependencies (installed automatically via `pip`).

---

## What this is good for

| Use case | Notes |
|----------|-------|
| **Prototyping a new nodalization** | Build a FILL → PIPE → BREAK skeleton quickly; iterate on cell count and geometry |
| **Translating an existing TRCIN** | Import ASCII, inspect components, regenerate with corrections |
| **Component-level test cases** | Isolated subsystem models (single SG leg, accumulator line, break segment) |
| **Parameter studies** | Script many similar models with varying geometry or boundary conditions |
| **Learning TRACE model structure** | Interactive Q&A about what properties each component type needs |
| **Generating reconstruction prompts** | The test runner produces `_prompt.md` and `_recipe.md` for any imported model |

---

## What it is NOT a replacement for

- **Full plant models** — Possible in principle, but a complete 4-loop PWR has hundreds of components and thousands of connections. Build subsystems first, assemble by hand in SNAP GUI.
- **Final QA-ready production models** — Always review the exported TRCIN against the [TRACE PWR/BWR Modeling Guidance](https://nrc-research.github.io/TRACE_guidance/) before using results analytically.
- **VESSEL (3-D reactor vessel) nodalization** — The MCP can create a VESSEL component but detailed per-cell/per-ring initialization is not yet supported.
- **PARCS kinetics coupling** — Not implemented.
- **Restart file manipulation** — Open and inspect `.med` files; restart deck editing must be done manually.
- **Replacing the SNAP GUI** — The GUI has visualization, drag-and-drop connection editing, and real-time validation feedback. Use it for complex topologies; use the MCP for scripted construction and inspection.

---

## Best practices

### Always start from the guidance
Before building any PWR or BWR component, consult the NRC modeling guidelines:

**https://nrc-research.github.io/TRACE_guidance/**

Key sections:
- [General Guidance](https://nrc-research.github.io/TRACE_guidance/pwr/general-guidance/) — NFF, KFAC, EPSW, volume ratio rules
- [Heat Structures](https://nrc-research.github.io/TRACE_guidance/pwr/heat-structures/) — radial nodes, material numbers, geometry type
- [Initialization](https://nrc-research.github.io/TRACE_guidance/pwr/initialization/) — steady-state procedure, pressure boundary setup
- [Break Modeling](https://nrc-research.github.io/TRACE_guidance/pwr/break-modeling/) — DEG vs split, nodalization criteria near break
- [Component Numbering](https://nrc-research.github.io/TRACE_guidance/pwr/component-numbering/) — NRC standard scheme (1000–1999 T-H, 100–999 fuel HTSTR)

The MCP resources `trace://reference/materials`, `trace://reference/friction`, and `trace://reference/component-numbering` contain extracted summaries of these sections and are visible to the AI during a session.

### Use guidance defaults — don't leave parameters Unknown

| Component | Parameter | Guidance default |
|-----------|-----------|-----------------|
| BREAK / FILL | `dxin` | `1e-6` m |
| BREAK / FILL | `volin` | `1e6` m³ |
| BREAK | `rbmx` | `1e20` |
| BREAK | `isat` | always `3` (T_sat) |
| PIPE | `epsw` | `4.572e-5` m (steel), `1.524e-6` m (SG drawn tubing) |

### Choose materials from the standard table

| SNAP name | Material | Use for |
|-----------|----------|---------|
| Material 1 | UO₂ | Fuel pellet |
| Material 2 | Zircaloy | Fuel cladding, thimble tubes |
| Material 8 | Stainless steel | General structures |
| Material 9 | Carbon steel | RPV barrel/baffle/shell, SG barrel |
| Material 12 | Inconel 600 | SG U-tubes, OTSG tubes |

### Heat structure radial nodes

| Structure | Nodes |
|-----------|-------|
| Fuel rods | 8 (5 pellet + gap + 2 clad) |
| SG tubes (Inconel) | 4 |
| RPV / SG barrel | wall_thickness_inches / 0.1 + 1 |

### Build and validate incrementally

1. Add boundary conditions first (FILL, BREAK)
2. Add hydraulic components (PIPE, PUMP, VALVE, TEE)
3. Connect hydraulic topology with `connect_components()`
4. Add heat structures
5. Wire surfaces with `connect_heat_structure()`
6. Call `validate_model()` — fix any errors before export
7. Call `export_trcin()` — review the TRCIN before running TRACE

---

## Installation & Registration

### 1. Installation
Install the root project dependencies (requires SNAP installation):
```bash
pip install -e .
```

### 2. Register with Claude Code
```bash
claude mcp add snap-trace \
  -e SNAP_PYTHON_PATH=/path/to/run-snap500/python \
  -- python /path/to/SNAP-MCP/mcp_server.py
```

### 3. Register with Claude Desktop
Add under `mcpServers` in your desktop configuration (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "snap-trace": {
      "command": "python3",
      "args": ["/path/to/SNAP-MCP/mcp_server.py"],
      "env": {
        "SNAP_PYTHON_PATH": "/path/to/run-snap500/python"
      }
    }
  }
}
```

---

## Tools Exposed

| Tool | Purpose |
|------|---------|
| `snap_status` | Check if SNAP/MEBatch is ready |
| `create_model` | Start a new empty model |
| `open_med_model` | Open an existing `.med` file |
| `import_trcin` | Import a TRACE ASCII input deck |
| `list_models` | List all models in the session registry |
| `get_component_schema` | Describe a component type's properties and guidance |
| `add_component` | Add a component to the model |
| `set_component_property` | Set a property on an existing component |
| `list_components` | List all components in a model |
| `get_component` | Inspect all readable properties of one component |
| `connect_components` | Wire a hydraulic junction between two components |
| `connect_heat_structure` | Couple an HS axial cell surface to a hydraulic component |
| `set_vessel_table` | Set per-cell ICs or edge HDs on a VESSEL via its 3-D property tables |
| `get_connections` | Show all junction connections in the model |
| `validate_model` | Run SNAP's export check (errors and warnings) |
| `export_trcin` | Export the model as a TRACE ASCII input deck |
| `save_med` | Save the model as a SNAP `.med` file |

---

## Resources Exposed

| URI | Contents |
|-----|---------|
| `trace://workflow/new-model` | Step-by-step build workflow |
| `trace://component-types` | All supported component types |
| `trace://connection-syntax` | How junctions work |
| `trace://enum-reference` | Common enum class names and values |
| `trace://reference/materials` | Material numbers, roughness, HS node counts |
| `trace://reference/friction` | NFF/KFAC guidance, 10:1 volume ratio rule |
| `trace://reference/component-numbering` | NRC standard PWR numbering scheme |
| `trace://example/standpipe` | Complete standpipe example script |
