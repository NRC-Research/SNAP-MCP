# Model Summary: BreakEnthalpy
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 2 | inlet pipe |
| PIPE | 3 | heater u-tube bank |
| PIPE | 4 | outlet pipe |
| FILL | 5 | fw outlet bc |
| BREAK | 1 | fw inlet bc |
| SIGNAL_VARIABLE | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 2 | inlet | ('[JUN1] Inlet', 1, 1) |
| PIPE 2 | outlet | ('[JUN1] Inlet', 3, 1) |
| PIPE 3 | inlet | ('', 2, 2) |
| PIPE 3 | outlet | ('[JUN1] Inlet', 4, 1) |
| PIPE 4 | inlet | ('', 3, 9) |
| PIPE 4 | outlet | ('', 5, 1) |
| FILL 5 | inlet | ('[JUN2] Outlet', 4, 2) |
| BREAK 1 | inlet | ('[JUN1] Inlet', 2, 1) |

## Key Properties

### PIPE 2
- `cells`: [Cell 1]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 8.2913 m
- **dx per cell:** [8.2913] m
- **Hydraulic diameter:** 0.04625 m

### PIPE 3
- `cells`: [Cell 1,Cell 2,Cell 3,Cell 4,Cell 5,Cell 6,Cell 7,Cell 8]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 66.3304 m
- **dx per cell:** [8.2913, 8.2913, 8.2913, 8.2913, 8.2913, 8.2913, 8.2913, 8.2913] m
- **Hydraulic diameter:** 0.04625 m

### PIPE 4
- `cells`: [Cell 1]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 8.2913 m
- **dx per cell:** [8.2913] m
- **Hydraulic diameter:** 0.04625 m

### FILL 5
- `pin`: 410.0
- `tlin`: 342.7
- `tvin`: 342.7
- `flowin`: 7936.64
- `alpin`: 0.0
- `ifty`: FillIftySel.Constant_Mass_Flow
- `dxin`: 8.2913
- `volin`: 0.013929

### BREAK 1
- `pin`: 410.0
- `tin`: 342.7
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 8.2913
- `volin`: 0.013929

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0
