# TRACE Model: 2hscase.1.old

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Hydraulic pipes

**CC 10 — 10$ sg primary tube bundle**: 4-cell pipe, 4.0 m long, 16.0 mm hydraulic diameter, wall roughness 1.0E-6 m.

**CC 20 — 20$ sg secondary-side boiler**: 3-cell pipe, 3.0 m long, 6.0 mm hydraulic diameter, wall roughness 1.0E-6 m.

## Boundary conditions

**CC 8 — 8$ primary flow boundary** (FILL): constant mass flow, 5000.0 kg/s, 1.55E7 Pa, 590.0 K inlet temperature.

**CC 18 — 18$ secondary fill boundary** (FILL): constant mass flow, 2500.0 kg/s, 5.5E6 Pa, 400.0 K inlet temperature.

**CC 12 — 12$ primary break boundary** (BREAK): pressure boundary at 1.55E7 Pa, 549.1 K.

**CC 22 — 22$ secondary break boundary** (BREAK): pressure boundary at 5.5E6 Pa, 400.0 K.

## Heat structures

**CC 900 — 900$ upflow sg tube bundle hs** (cylindrical heat structure): 2 axial zones, 2.0 m total, 3 radial mesh points, inner radius 8.0E-3 m, wall thickness 1.0E-3 m, material Material 12, initialized at 549.3 K.
  - Inner surface → CC 10 cells 1, 2
  - Outer surface → CC 20 cells 1, 2

**CC 910 — 910$ downflow sg tube bundle hs** (cylindrical heat structure): 2 axial zones, 2.0 m total, 3 radial mesh points, inner radius 8.0E-3 m, wall thickness 1.0E-3 m, material Material 12, initialized at 549.3 K.
  - Inner surface → CC 10 cells 3, 4
  - Outer surface → CC 20 cells 2, 1

## Flow topology

- CC 10 (10$ sg primary tube bundle) **inlet** → CC 8 (8$ primary flow boundary), cell 1
- CC 10 (10$ sg primary tube bundle) **outlet** → CC 12 (12$ primary break boundary), cell 1
- CC 20 (20$ sg secondary-side boiler) **inlet** → CC 18 (18$ secondary fill boundary), cell 1
- CC 20 (20$ sg secondary-side boiler) **outlet** → CC 22 (22$ secondary break boundary), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 10 | PIPE | 10$ sg primary tube bundle |
| 20 | PIPE | 20$ sg secondary-side boiler |
| 8 | FILL | 8$ primary flow boundary |
| 18 | FILL | 18$ secondary fill boundary |
| 12 | BREAK | 12$ primary break boundary |
| 22 | BREAK | 22$ secondary break boundary |
| 900 | HEAT_STRUCTURE | 900$ upflow sg tube bundle hs |
| 910 | HEAT_STRUCTURE | 910$ downflow sg tube bundle hs |
| 1 | SIGNAL_VARIABLE | unnamed |
| 1 | TRIP | unnamed |

