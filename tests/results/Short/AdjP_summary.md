# Model Summary: AdjP
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 701 | one cell pipe |
| BREAK | 201 | side leg one bc |
| BREAK | 100 | side leg one bc |
| SIGNAL_VARIABLE | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 701 | inlet | ('[JUN1] Inlet', 100, 1) |
| PIPE 701 | outlet | ('[JUN1] Inlet', 201, 1) |
| BREAK 201 | inlet | ('', 701, 3) |
| BREAK 100 | inlet | ('[JUN1] Inlet', 701, 1) |

## Key Properties

### PIPE 701
- `cells`: [Cell 1,Cell 2]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 2.0 m
- **dx per cell:** [1.0, 1.0] m
- **Hydraulic diameter:** 1.0 m

### BREAK 201
- `pin`: 2.0E5
- `tin`: 600.0
- `alpin`: 1.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.Input_Pressure_Table
- `dxin`: 1.0
- `volin`: 0.1

### BREAK 100
- `pin`: 2.0E5
- `tin`: 600.0
- `alpin`: 1.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.0
- `volin`: 0.1

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0
