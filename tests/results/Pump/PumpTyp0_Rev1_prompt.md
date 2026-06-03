# TRACE Model: PumpTyp0_Rev1

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

**Purpose:** #    Same as test problem PumpTyp0, except NPMPSD was changed from -1 to 2.
#    Signal variable 2 is trip status for trip 11.
#    Trip 11 is initially off, then goes on at 100 secs and then off again at 300 secs.
#

## Hydraulic pipes

**CC 14 — pipe-to-pump**: 2-cell pipe, 10.0 m long, 1128.4 mm hydraulic diameter.

**CC 13 — 13$ int-loop pump** (PUMP): see original model for pump curve and geometry.

## Flow topology

- CC 14 (pipe-to-pump) **inlet** → CC 13 (13$ int-loop pump), cell 3

## Component number reference

| CC | Type | Name |
|---|---|---|
| 14 | PIPE | pipe-to-pump |
| 13 | PUMP | 13$ int-loop pump |
| -1 | CONTROL_BLOCK | unnamed |
| 1 | SIGNAL_VARIABLE | unnamed |
| 2 | SIGNAL_VARIABLE | unnamed |
| 11 | TRIP | unnamed |

