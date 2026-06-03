# TRACE Model: BreakEnthalpy

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 2 — inlet pipe**: 1-cell pipe, 8.2913 m long, 46.2 mm hydraulic diameter.

**CC 3 — heater u-tube bank**: 8-cell pipe, 66.3304 m long, 46.2 mm hydraulic diameter.

**CC 4 — outlet pipe**: 1-cell pipe, 8.2913 m long, 46.2 mm hydraulic diameter.

## Boundary conditions

**CC 5 — fw outlet bc** (FILL): constant mass flow, 7936.64 kg/s, 410.0 Pa, 342.7 K inlet temperature.

**CC 1 — fw inlet bc** (BREAK): pressure boundary at 410.0 Pa, 342.7 K.

## Flow topology

- CC 2 (inlet pipe) **inlet** → CC 1 (fw inlet bc), cell 1
- CC 2 (inlet pipe) **outlet** → CC 3 (heater u-tube bank), cell 1
- CC 3 (heater u-tube bank) **outlet** → CC 4 (outlet pipe), cell 1
- CC 4 (outlet pipe) **outlet** → CC 5 (fw outlet bc), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 2 | PIPE | inlet pipe |
| 3 | PIPE | heater u-tube bank |
| 4 | PIPE | outlet pipe |
| 5 | FILL | fw outlet bc |
| 1 | BREAK | fw inlet bc |
| 1 | SIGNAL_VARIABLE | unnamed |

