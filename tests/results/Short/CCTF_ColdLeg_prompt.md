# TRACE Model: CCTF_ColdLeg

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 21 — Cold Leg**: 5-cell pipe, 4.1719 m long, 155.2 mm hydraulic diameter, wall roughness 5.0E-6 m.

## Boundary conditions

**CC 11 — steam fill** (FILL): FillIftySel.Mass_FLow_Table, 0.688 kg/s, 2.45E5 Pa, 399.9 K inlet temperature.

**CC 12 — water fill** (FILL): FillIftySel.Mass_FLow_Table, 0.0 kg/s, 2.45E5 Pa, 309.2 K inlet temperature.

**CC 31 — Press BC** (BREAK): pressure boundary at 2.45E5 Pa, 405.0 K.

## Flow topology

- CC 21 (Cold Leg) **inlet** → CC 11 (steam fill), cell 1
- CC 21 (Cold Leg) **outlet** → CC 31 (Press BC), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 21 | PIPE | Cold Leg |
| 11 | FILL | steam fill |
| 12 | FILL | water fill |
| 31 | BREAK | Press BC |
| 1 | SIGNAL_VARIABLE | time |

