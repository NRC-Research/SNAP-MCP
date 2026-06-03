# Model Summary: ptpL0a
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 700 | inlet end main leg |
| PIPE | 702 | outlet end main leg |
| FILL | 100 | mass flow bc |
| FILL | 101 | mass flow bc |
| BREAK | 201 | side leg one bc |
| TEE | 701 | the tee |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 700 | inlet | ('', 100, 1) |
| PIPE 700 | outlet | ('[JUN1] Inlet', 701, 1) |
| PIPE 702 | inlet | ('', 701, 2) |
| PIPE 702 | outlet | ('[JUN1] Inlet', 201, 1) |
| FILL 100 | inlet | ('', 700, 1) |
| FILL 101 | inlet | ('', 701, 5) |
| BREAK 201 | inlet | ('', 702, 3) |
| TEE 701 | inlet | ('', 700, 3) |

## Key Properties

### PIPE 700
- `cells`: [Cell 1,Cell 2]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 3.0 m
- **dx per cell:** [1.5, 1.5] m
- **Hydraulic diameter:** 1.0 m

### PIPE 702
- `cells`: [Cell 1,Cell 2]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 5.0 m
- **dx per cell:** [2.5, 2.5] m
- **Hydraulic diameter:** 1.0 m

### FILL 100
- `pin`: 1.0E5
- `tlin`: 300.0
- `tvin`: 300.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Constant_Velocity
- `dxin`: 1.5
- `volin`: 0.15

### FILL 101
- `pin`: 1.0E5
- `tlin`: 370.0
- `tvin`: 370.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Constant_Velocity
- `dxin`: 0.5
- `volin`: 0.1

### BREAK 201
- `pin`: 1.0E5
- `tin`: 300.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 2.5
- `volin`: 0.75

### TEE 701
- `name`: the tee
