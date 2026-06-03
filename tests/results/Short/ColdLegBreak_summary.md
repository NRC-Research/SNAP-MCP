# Model Summary: ColdLegBreak
## Components

| Type | CC# | Name |
|---|---|---|
| BREAK | 25 | $25$ cold leg left BC |
| BREAK | 30 | $30$ cold leg right BC |
| BREAK | 229 | $229$ small break pressure boundary |
| TEE | 29 | $29$ cold leg section 2c |
| SIGNAL_VARIABLE | 1 | unnamed |
| TRIP | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| BREAK 25 | inlet | ('[JUN1] Inlet', 29, 1) |
| BREAK 30 | inlet | ('', 29, 3) |
| BREAK 229 | inlet | ('', 29, 5) |
| TEE 29 | inlet | ('[JUN1] Inlet', 25, 1) |

## Key Properties

### BREAK 25
- `pin`: 5.91E6
- `tin`: 547.8
- `alpin`: 0.5
- `isat`: BreakIsatSel.Set_liquid_and_gas_to_Tsat
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.1033
- `volin`: 0.42278

### BREAK 30
- `pin`: 5.91E6
- `tin`: 547.8
- `alpin`: 0.5
- `isat`: BreakIsatSel.Set_liquid_and_gas_to_Tsat
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.1033
- `volin`: 0.42278

### BREAK 229
- `pin`: 1.0135E5
- `tin`: 373.2
- `alpin`: 1.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Define_the_Initial_State
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 0.06668
- `volin`: 4.0348E-4

### TEE 29
- `name`: $29$ cold leg section 2c

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0

### TRIP 1
