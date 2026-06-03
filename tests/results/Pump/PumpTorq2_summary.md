# Model Summary: PumpTorq2
**Purpose:** #     pump motor torque test problem - IPMPTY = 3.
#     This test is identical to regression problem PumpTorq with
#     the added feature of the pump motor torque.  The pump motor
#     torque comes from control block id -680.
#

## Components

| Type | CC# | Name |
|---|---|---|
| BREAK | 702 | bottom break |
| BREAK | 701 | bottom break |
| PUMP | 700 | pump no. 2 |
| CONTROL_BLOCK | -680 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |
| SIGNAL_VARIABLE | 2 | unnamed |
| SIGNAL_VARIABLE | 3 | unnamed |
| TRIP | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| BREAK 702 | inlet | ('', 700, 3) |
| BREAK 701 | inlet | ('[JUN1] Inlet', 700, 1) |
| PUMP 700 | inlet | ('[JUN1] Inlet', 701, 1) |
| PUMP 700 | outlet | ('[JUN1] Inlet', 702, 1) |

## Key Properties

### BREAK 702
- `pin`: 1.0E6
- `tin`: 373.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 0.3
- `volin`: 0.09

### BREAK 701
- `pin`: 1.0E6
- `tin`: 373.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 0.3
- `volin`: 0.09

### PUMP 700
- `name`: pump no. 2
- `ipmpty`: 3

### CONTROL_BLOCK -680
- `name`: unnamed
- `control_type`: ControlTypeSel.Constant
- `cbgain`: 1.0
- `cbxmin`: -1.0E4
- `cbxmax`: 1.0E4
- `cbcon1`: 500.0
- `cbcon2`: 1000.0

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0

### SIGNAL_VARIABLE 2
- `name`: unnamed
- `connection`: 700
- `icn1`: 0

### SIGNAL_VARIABLE 3
- `name`: unnamed
- `connection`: 700
- `icn1`: 0

### TRIP 1
