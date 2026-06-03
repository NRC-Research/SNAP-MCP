# TRACE Model: AdjP

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 701 — one cell pipe**: 2-cell pipe, 2.0 m long, 1000.0 mm hydraulic diameter.

## Boundary conditions

**CC 201 — side leg one bc** (BREAK): pressure boundary at 2.0E5 Pa, 600.0 K.

**CC 100 — side leg one bc** (BREAK): pressure boundary at 2.0E5 Pa, 600.0 K.

## Flow topology

- CC 701 (one cell pipe) **inlet** → CC 100 (side leg one bc), cell 1
- CC 701 (one cell pipe) **outlet** → CC 201 (side leg one bc), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 701 | PIPE | one cell pipe |
| 201 | BREAK | side leg one bc |
| 100 | BREAK | side leg one bc |
| 1 | SIGNAL_VARIABLE | unnamed |

