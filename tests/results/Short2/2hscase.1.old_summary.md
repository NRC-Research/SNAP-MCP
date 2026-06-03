# Model Summary: 2hscase.1.old
## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 10 | $10$ sg primary tube bundle |
| PIPE | 20 | $20$ sg secondary-side boiler |
| FILL | 8 | $8$ primary flow boundary |
| FILL | 18 | $18$ secondary fill boundary |
| BREAK | 12 | $12$ primary break boundary |
| BREAK | 22 | $22$ secondary break boundary |
| HEAT_STRUCTURE | 900 | $900$ upflow sg tube bundle hs |
| HEAT_STRUCTURE | 910 | $910$ downflow sg tube bundle hs |
| SIGNAL_VARIABLE | 1 | unnamed |
| TRIP | 1 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 10 | inlet | ('', 8, 1) |
| PIPE 10 | outlet | ('[JUN1] Inlet', 12, 1) |
| PIPE 20 | inlet | ('', 18, 1) |
| PIPE 20 | outlet | ('[JUN1] Inlet', 22, 1) |
| FILL 8 | inlet | ('', 10, 1) |
| FILL 18 | inlet | ('', 20, 1) |
| BREAK 12 | inlet | ('', 10, 5) |
| BREAK 22 | inlet | ('', 20, 4) |

## Key Properties

### PIPE 10
- `cells`: [Cell 1,Cell 2,Cell 3,Cell 4]
- `fluid_segment`: Main Tube
- `epsw`: 1.0E-6
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 4.0 m
- **dx per cell:** [1.0, 1.0, 1.0, 1.0] m
- **Hydraulic diameter:** 0.016 m

### PIPE 20
- `cells`: [Cell 1,Cell 2,Cell 3]
- `fluid_segment`: Main Tube
- `epsw`: 1.0E-6
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 3.0 m
- **dx per cell:** [1.0, 1.0, 1.0] m
- **Hydraulic diameter:** 0.006 m

### FILL 8
- `pin`: 1.55E7
- `tlin`: 590.0
- `tvin`: 590.0
- `flowin`: 5000.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Constant_Mass_Flow
- `dxin`: 1.0
- `volin`: 1.0

### FILL 18
- `pin`: 5.5E6
- `tlin`: 400.0
- `tvin`: 400.0
- `flowin`: 2500.0
- `alpin`: 0.0
- `ifty`: FillIftySel.Constant_Mass_Flow
- `dxin`: 1.0
- `volin`: 4.0

### BREAK 12
- `pin`: 1.55E7
- `tin`: 549.1
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.0
- `volin`: 1.0

### BREAK 22
- `pin`: 5.5E6
- `tin`: 400.0
- `alpin`: 0.0
- `isat`: BreakIsatSel.Enter_liquid_gas_temp
- `ioff`: BreakIoffSel.Last_Interp_State_Held_Const
- `ibty`: BreakIbtySel.No_Tables
- `dxin`: 1.0
- `volin`: 4.0

### HEAT_STRUCTURE 900
- `hscyl`: 1
- `inner_radius`: 8.0E-3
- `th`: 1.0E-3
- `hgapo`: 0.0
- `ichf`: 1
- `iaxcnd`: True
- `nofuelrod`: HSFuelSel.Not_Fuel_Rod
- `nfci`: 0
- `nfcil`: 1
- `dhtstrz`: [1.0,1.0]
- `rftn_table`: [549.3,549.3,549.3]
[549.3,549.3,549.3]

- **Radial mesh layers:**
  - Layer 1: material=Material 12, thickness=0.0009999999999999992 m, nodes=2
- **HS-fluid connections (first 3 cells shown):**
  - Cell 1: inner→CC10 cell 1, outer→CC20 cell 1
  - Cell 2: inner→CC10 cell 2, outer→CC20 cell 2

### HEAT_STRUCTURE 910
- `hscyl`: 1
- `inner_radius`: 8.0E-3
- `th`: 1.0E-3
- `hgapo`: 0.0
- `ichf`: 1
- `iaxcnd`: True
- `nofuelrod`: HSFuelSel.Not_Fuel_Rod
- `nfci`: 0
- `nfcil`: 1
- `dhtstrz`: [1.0,1.0]
- `rftn_table`: [549.3,549.3,549.3]
[549.3,549.3,549.3]

- **Radial mesh layers:**
  - Layer 1: material=Material 12, thickness=0.0009999999999999992 m, nodes=2
- **HS-fluid connections (first 3 cells shown):**
  - Cell 1: inner→CC10 cell 3, outer→CC20 cell 2
  - Cell 2: inner→CC10 cell 4, outer→CC20 cell 1

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0

### TRIP 1
