# TRACE Model: PumpTorq3

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

**Purpose:** #     pump motor torque test problem - IPMPTY = 3.
#     This test is identical to PumpTorq2 with the added feature
#     that IPMPTR points to trip 1.  Initial motor torque will be
#     1000 N-m before trip and then 500 N-m after trip.
#

## Boundary conditions

**CC 702 — bottom break** (BREAK): pressure boundary at 1.0E6 Pa, 373.0 K.

**CC 701 — bottom break** (BREAK): pressure boundary at 1.0E6 Pa, 373.0 K.

**CC 700 — pump no. 2** (PUMP): see original model for pump curve and geometry.

## Flow topology

- CC 702 (bottom break) **inlet** → CC 700 (pump no. 2), cell 3
- CC 701 (bottom break) **inlet** → CC 700 (pump no. 2), cell 1

## Component number reference

| CC | Type | Name |
|---|---|---|
| 702 | BREAK | bottom break |
| 701 | BREAK | bottom break |
| 700 | PUMP | pump no. 2 |
| -680 | CONTROL_BLOCK | unnamed |
| 1 | SIGNAL_VARIABLE | unnamed |
| 2 | SIGNAL_VARIABLE | unnamed |
| 3 | SIGNAL_VARIABLE | unnamed |
| 1 | TRIP | unnamed |

