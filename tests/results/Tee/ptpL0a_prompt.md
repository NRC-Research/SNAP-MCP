# TRACE Model: ptpL0a

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 700 — inlet end main leg**: 2-cell pipe, 3.0 m long, 1000.0 mm hydraulic diameter.

**CC 702 — outlet end main leg**: 2-cell pipe, 5.0 m long, 1000.0 mm hydraulic diameter.

## Boundary conditions

**CC 100 — mass flow bc** (FILL): FillIftySel.Constant_Velocity, ? kg/s, 1.0E5 Pa, 300.0 K inlet temperature.

**CC 101 — mass flow bc** (FILL): FillIftySel.Constant_Velocity, ? kg/s, 1.0E5 Pa, 370.0 K inlet temperature.

**CC 201 — side leg one bc** (BREAK): pressure boundary at 1.0E5 Pa, 300.0 K.

**CC 701 — the tee** (TEE): three-way junction.

## Flow topology

- CC 700 (inlet end main leg) **inlet** → CC 100 (mass flow bc), cell 1
- CC 700 (inlet end main leg) **outlet** → CC 701 (the tee), cell 1
- CC 702 (outlet end main leg) **inlet** → CC 701 (the tee), cell 2
- CC 702 (outlet end main leg) **outlet** → CC 201 (side leg one bc), cell 1
- CC 101 (mass flow bc) **inlet** → CC 701 (the tee), cell 5

## Component number reference

| CC | Type | Name |
|---|---|---|
| 700 | PIPE | inlet end main leg |
| 702 | PIPE | outlet end main leg |
| 100 | FILL | mass flow bc |
| 101 | FILL | mass flow bc |
| 201 | BREAK | side leg one bc |
| 701 | TEE | the tee |

