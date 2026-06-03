# Model Summary: CCTF_ColdLeg
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 21 | Cold Leg |
| FILL | 11 | steam fill |
| FILL | 12 | water fill |
| BREAK | 31 | Press BC |
| SIGNAL_VARIABLE | 1 | time |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 21 | inlet | ('', 11, 1) |
| PIPE 21 | outlet | ('[JUN1] Inlet', 31, 1) |
| FILL 11 | inlet | ('', 21, 1) |
| FILL 12 | inlet | ('Crossflow', 21, 2, 45.0) |
| BREAK 31 | inlet | ('', 21, 6) |

## Key Properties

### PIPE 21
- `cells`: [Cell 1,Cell 2,Cell 3,Cell 4,Cell 5]
- `fluid_segment`: Main Tube
- `epsw`: 5.0E-6
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 4.1719 m
- **dx per cell:** [0.8, 0.8, 0.8573, 0.8573, 0.8573] m
- **Hydraulic diameter:** 0.1552 m

### FILL 11
- `pin`: 2.45E5
- `tlin`: 399.9
- `tvin`: 405.0
- `flowin`: 0.688
- `alpin`: 1.0
- `ifty`: FillIftySel.Mass_FLow_Table
- `dxin`: 1.0
- `volin`: 0.01892

### FILL 12
- `pin`: 2.45E5
- `tlin`: 309.2
- `tvin`: 399.9
- `flowin`: 0.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Mass_FLow_Table
- `dxin`: 1.0
- `volin`: 1.735E-3

### BREAK 31
- `pin`: 2.45E5
- `tin`: 405.0
- `alpin`: 1.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Define_the_Initial_State
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.0
- `volin`: 0.01892

### SIGNAL_VARIABLE 1
- `name`: time
- `icn1`: 0
