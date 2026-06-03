# TRACE Model: CBValveCvSJC

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 510 — inlet**: 1-cell pipe, 0.3 m long, 618.0 mm hydraulic diameter.

**CC 520 — exit**: 1-cell pipe, 0.3 m long, 618.0 mm hydraulic diameter.

## Boundary conditions

**CC 436 — inlet** (BREAK): pressure boundary at 1.2E6 Pa, 300.0 K.

**CC 666 — exit** (BREAK): pressure boundary at 1.0E6 Pa, 300.0 K.

**CC 515 — chk vlv** (VALVE): see original model.

## Flow topology

- CC 510 (inlet) **inlet** → CC 456 (456), cell 1
- CC 510 (inlet) **outlet** → CC 515 (chk vlv), cell 1
- CC 520 (exit) **inlet** → CC 515 (chk vlv), cell 1
- CC 520 (exit) **outlet** → CC 656 (656), cell 1
- CC 436 (inlet) **inlet** → CC 456 (456), cell 1
- CC 666 (exit) **inlet** → CC 656 (656), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 510 | PIPE | inlet |
| 520 | PIPE | exit |
| 436 | BREAK | inlet |
| 666 | BREAK | exit |
| 515 | VALVE | chk vlv |
| -329 | CONTROL_BLOCK | unnamed |
| -331 | CONTROL_BLOCK | unnamed |
| 1 | SIGNAL_VARIABLE | unnamed |

