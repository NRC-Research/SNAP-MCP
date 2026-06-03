# TRACE Model: CBValveCv

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Boundary conditions

**CC 436 — inlet** (BREAK): pressure boundary at 1.2E6 Pa, 300.0 K.

**CC 666 — exit** (BREAK): pressure boundary at 1.0E6 Pa, 300.0 K.

**CC 515 — chk vlv** (VALVE): see original model.

## Flow topology

- CC 436 (inlet) **inlet** → CC 515 (chk vlv), cell 1
- CC 666 (exit) **inlet** → CC 515 (chk vlv), cell 3

## Component number reference

| CC | Type | Name |
|---|---|---|
| 436 | BREAK | inlet |
| 666 | BREAK | exit |
| 515 | VALVE | chk vlv |
| -329 | CONTROL_BLOCK | unnamed |
| -331 | CONTROL_BLOCK | unnamed |
| 1 | SIGNAL_VARIABLE | unnamed |

