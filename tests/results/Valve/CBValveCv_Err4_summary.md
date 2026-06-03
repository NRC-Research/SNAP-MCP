# Model Summary: CBValveCv_Err4
## Components

| Type | CC# | Name |
|---|---|---|
| BREAK | 436 | inlet |
| BREAK | 666 | exit |
| VALVE | 515 | chk vlv |
| CONTROL_BLOCK | -329 | unnamed |
| CONTROL_BLOCK | -331 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| BREAK 436 | inlet | ('[JUN1] Inlet', 515, 1) |
| BREAK 666 | inlet | ('', 515, 3) |
| VALVE 515 | inlet | ('[JUN1] Inlet', 436, 1) |
| VALVE 515 | outlet | ('[JUN1] Inlet', 666, 1) |

## Key Properties

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
