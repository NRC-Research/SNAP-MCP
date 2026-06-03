# TRACE Model: CONTAN5

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

**Purpose:** #    Same as test problem CONTAN4, except added legacycontm = .false. to namelist input
#    and added the addition input required for the CONTAN component.
#

## Hydraulic pipes

**CC 2 — Primary side PIPE**: 12-cell pipe, 12.0 m long, 1000.0 mm hydraulic diameter, wall roughness 1.0E-5 m.

## Boundary conditions

**CC 1 — channel inlet flow bc** (FILL): FillIftySel.Mass_FLow_Table, 0.0 kg/s, 1.0E7 Pa, 584.1 K inlet temperature.

**CC 3 — channel downstream pressure bc** (BREAK): pressure boundary at 1.0E5 Pa, 300.0 K.

**CC 103** (CONTAN_COMPARTMENT): see original model.

## Flow topology

- CC 2 (Primary side PIPE) **inlet** → CC 1 (channel inlet flow bc), cell 1
- CC 2 (Primary side PIPE) **outlet** → CC 3 (channel downstream pressure bc), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 2 | PIPE | Primary side PIPE |
| 1 | FILL | channel inlet flow bc |
| 3 | BREAK | channel downstream pressure bc |
| -1 | CONTROL_BLOCK | unnamed |
| -2 | CONTROL_BLOCK | unnamed |
| 1 | SIGNAL_VARIABLE | unnamed |
| 2 | SIGNAL_VARIABLE | unnamed |
| 3 | SIGNAL_VARIABLE | unnamed |
| 1001 | TRIP | unnamed |
| 103 | CONTAN_COMPARTMENT | unnamed |

