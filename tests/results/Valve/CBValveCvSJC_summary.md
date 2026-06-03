# Model Summary: CBValveCvSJC
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 510 | inlet |
| PIPE | 520 | exit |
| BREAK | 436 | inlet |
| BREAK | 666 | exit |
| VALVE | 515 | chk vlv |
| CONTROL_BLOCK | -329 | unnamed |
| CONTROL_BLOCK | -331 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 510 | inlet | ('', 456, 1) |
| PIPE 510 | outlet | ('', 515, 1) |
| PIPE 520 | inlet | ('', 515, 1) |
| PIPE 520 | outlet | ('', 656, 1) |
| BREAK 436 | inlet | ('[JUN1] Inlet', 456, 1) |
| BREAK 666 | inlet | ('', 656, 1) |
| VALVE 515 | inlet | ('[JUN2] Outlet', 510, 1) |
| VALVE 515 | outlet | ('[JUN1] Inlet', 520, 1) |

## Key Properties

### PIPE 510
- `cells`: [Cell 1]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 0.3 m
- **dx per cell:** [0.3] m
- **Hydraulic diameter:** 0.6180387 m

### PIPE 520
- `cells`: [Cell 1]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 0.3 m
- **dx per cell:** [0.3] m
- **Hydraulic diameter:** 0.6180387 m

### BREAK 436
- `pin`: 1.2E6
- `tin`: 300.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Use_separate_tables_or_CS
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.Opt_3_plus_NC_Gas_PP_Table
- `dxin`: 0.3
- `volin`: 0.09

### BREAK 666
- `pin`: 1.0E6
- `tin`: 300.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Use_separate_tables_or_CS
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.Opt_3_plus_NC_Gas_PP_Table
- `dxin`: 0.3
- `volin`: 0.09

### VALVE 515
- `name`: chk vlv

### CONTROL_BLOCK -329
- `name`: unnamed
- `control_type`: ControlTypeSel.Sum
- `cbgain`: 1.0
- `cbxmin`: -1.0E20
- `cbxmax`: 1.0E20
- `cbcon1`: 0.0
- `cbcon2`: 0.0

### CONTROL_BLOCK -331
- `name`: unnamed
- `control_type`: ControlTypeSel.Function
- `cbgain`: 1.0
- `cbxmin`: -1.0E20
- `cbxmax`: 1.0E20
- `cbcon1`: 0.0
- `cbcon2`: 0.0

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0
