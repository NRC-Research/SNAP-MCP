# TRACE Model: PumpTyp0

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

**Purpose:** #    Simple pump IPMPTY = 0 test.  Closed loop with single PIPE component
#    connected to inlet and outlet of PUMP.  Pump trip is initially off
#    then goes on at 100 seconds.  Stays on to 300 seconds and then goes
#    off.  When trip is off the volumetric flow through the pump is
#    6.5 m^3/s and when the trip is on the volumetric flow through the pump is
#    7 m^3/s.
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
| 11 | TRIP | unnamed |

