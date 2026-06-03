# TRACE Model: PumpTorq3R

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

**Purpose:** #     pump motor torque test problem - IPMPTY = 3.
#     Restarts from PumpTorq3 at time zero.  If time zero restart
#     dump is good then PumpTorq3 and PumpTorq3R should be the same.
#

## Component number reference

| CC | Type | Name |
|---|---|---|

