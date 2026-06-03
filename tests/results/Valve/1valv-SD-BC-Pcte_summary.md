# Model Summary: 1valv-SD-BC-Pcte
## Components

| Type | CC# | Name |
|---|---|---|
| BREAK | 1 | Linea de vapor |
| BREAK | 101 | Linea de vapor |
| VALVE | 21 | Valvula SD 538 |
| SIGNAL_VARIABLE | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| BREAK 1 | inlet | ('[JUN1] Inlet', 21, 1) |
| BREAK 101 | inlet | ('', 21, 3) |
| VALVE 21 | inlet | ('[JUN1] Inlet', 1, 1) |
| VALVE 21 | outlet | ('[JUN1] Inlet', 101, 1) |

## Key Properties

### BREAK 1
- `pin`: 6.6E6
- `tin`: 547.204
- `alpin`: 1.0
- `isat`: BreakIsatSel.Set_liquid_and_gas_to_Tsat
- `ioff`: BreakIoffSel.Define_the_Initial_State
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 0.1
- `volin`: 1.0E5

### BREAK 101
- `pin`: 1.0E5
- `tin`: 372.756
- `alpin`: 1.0
- `isat`: BreakIsatSel.Set_liquid_and_gas_to_Tsat
- `ioff`: BreakIoffSel.Define_the_Initial_State
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 0.1
- `volin`: 1.0E5

### VALVE 21
- `name`: Valvula SD 538

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0
