# TRACE Model: ColdLegBreak

Build this model using the snap-trace MCP tools. Start with `snap_status()` to confirm the connection, then `create_model()`. Use `get_component_schema()` before adding each new component type. Wire hydraulic junctions with `connect_components()`, heat structure surfaces with `connect_heat_structure()`, then finish with `validate_model()` and `export_trcin()`.

## Boundary conditions

**CC 25 — 25$ cold leg left BC** (BREAK): pressure boundary at 5.91E6 Pa, 547.8 K.

**CC 30 — 30$ cold leg right BC** (BREAK): pressure boundary at 5.91E6 Pa, 547.8 K.

**CC 229 — 229$ small break pressure boundary** (BREAK): pressure boundary at 1.0135E5 Pa, 373.2 K.

**CC 29 — 29$ cold leg section 2c** (TEE): three-way junction.

## Flow topology

- CC 25 (25$ cold leg left BC) **inlet** → CC 29 (29$ cold leg section 2c), cell 1
- CC 30 (30$ cold leg right BC) **inlet** → CC 29 (29$ cold leg section 2c), cell 3
- CC 229 (229$ small break pressure boundary) **inlet** → CC 29 (29$ cold leg section 2c), cell 5

## Component number reference

| CC | Type | Name |
|---|---|---|
| 25 | BREAK | 25$ cold leg left BC |
| 30 | BREAK | 30$ cold leg right BC |
| 229 | BREAK | 229$ small break pressure boundary |
| 29 | TEE | 29$ cold leg section 2c |
| 1 | SIGNAL_VARIABLE | unnamed |
| 1 | TRIP | unnamed |

