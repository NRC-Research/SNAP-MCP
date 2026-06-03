# Model Summary: CONTAN4
**Purpose:** #    Same as test problem CONTAN3, except region for BREAK 3 was changed from 0 to 2
#    and CONTAN ITRKL input was changed from 0 to 1.
#

## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 2 | Primary side PIPE |
| FILL | 1 | channel inlet flow bc |
| BREAK | 3 | channel downstream pressure bc |
| CONTROL_BLOCK | -1 | unnamed |
| CONTROL_BLOCK | -2 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |
| SIGNAL_VARIABLE | 2 | unnamed |
| SIGNAL_VARIABLE | 3 | unnamed |
| TRIP | 1001 | unnamed |
| CONTAN_COMPARTMENT | 103 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 2 | inlet | ('', 1, 1) |
| PIPE 2 | outlet | ('[JUN1] Inlet', 3, 1) |
| FILL 1 | inlet | ('', 2, 1) |
| BREAK 3 | inlet | ('', 2, 13) |

## Key Properties

### PIPE 2
- `cells`: [Cell 1,Cell 2,Cell 3,Cell 4,Cell 5,Cell 6,Cell 7,Cell 8,Cell 9,Cell 10,Cell 11,Cell 12]
- `fluid_segment`: Main Tube
- `epsw`: 1.0E-5
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 12.0 m
- **dx per cell:** [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] m
- **Hydraulic diameter:** 1.0 m

### FILL 1
- `pin`: 1.0E7
- `tlin`: 584.1
- `tvin`: 584.1
- `flowin`: 0.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Mass_FLow_Table
- `dxin`: 1.0
- `volin`: 2.0

### BREAK 3
- `pin`: 1.0E5
- `tin`: 300.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.CONTAN_Component
- `dxin`: 1.0
- `volin`: 0.1

### CONTROL_BLOCK -1
- `name`: unnamed
- `control_type`: ControlTypeSel.Multiply
- `cbgain`: 1.0
- `cbxmin`: 0.0
- `cbxmax`: 1.0E30
- `cbcon1`: 0.0
- `cbcon2`: 0.0

### CONTROL_BLOCK -2
- `name`: unnamed
- `control_type`: ControlTypeSel.Integrate
- `cbgain`: 1.0
- `cbxmin`: 0.0
- `cbxmax`: 1.0E30
- `cbcon1`: 0.0
- `cbcon2`: 0.0

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0

### SIGNAL_VARIABLE 2
- `name`: unnamed
- `icn1`: 0

### SIGNAL_VARIABLE 3
- `name`: unnamed
- `icn1`: 0

### TRIP 1001

### CONTAN_COMPARTMENT 103
- `name`: unnamed
- `rml`: 1000.0
- `itrkl`: OnOffSel.On
