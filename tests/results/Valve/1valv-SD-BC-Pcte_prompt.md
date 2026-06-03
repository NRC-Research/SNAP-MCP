# TRACE Model: 1valv-SD-BC-Pcte

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Boundary conditions

**CC 1 — Linea de vapor** (BREAK): pressure boundary at 6.6E6 Pa, 547.204 K.

**CC 101 — Linea de vapor** (BREAK): pressure boundary at 1.0E5 Pa, 372.756 K.

**CC 21 — Valvula SD 538** (VALVE): see original model.

## Flow topology

- CC 1 (Linea de vapor) **inlet** → CC 21 (Valvula SD 538), cell 1
- CC 101 (Linea de vapor) **inlet** → CC 21 (Valvula SD 538), cell 3

## Component number reference

| CC | Type | Name |
|---|---|---|
| 1 | BREAK | Linea de vapor |
| 101 | BREAK | Linea de vapor |
| 21 | VALVE | Valvula SD 538 |
| 1 | SIGNAL_VARIABLE | unnamed |

