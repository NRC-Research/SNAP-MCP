# Model Summary: PumpTyp0_Rev1
**Purpose:** #    Same as test problem PumpTyp0, except NPMPSD was changed from -1 to 2.
#    Signal variable 2 is trip status for trip 11.
#    Trip 11 is initially off, then goes on at 100 secs and then off again at 300 secs.
#

## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 14 | pipe-to-pump |
| PUMP | 13 | $13$ int-loop pump |
| CONTROL_BLOCK | -1 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |
| SIGNAL_VARIABLE | 2 | unnamed |
| TRIP | 11 | unnamed |

## Connections

| Component | Face | Connected to |
|---|---|---|
| PIPE 14 | inlet | ('', 13, 3) |
| PIPE 14 | outlet | ('[JUN1] Inlet', 13, 1) |
| PUMP 13 | inlet | ('', 14, 3) |
| PUMP 13 | outlet | ('[JUN1] Inlet', 14, 1) |

## Key Properties

### PIPE 14
- `cells`: [Cell 1,Cell 2]
- `fluid_segment`: Main Tube
- `epsw`: 0.0
- `calculation_flag`: CalculationFlag.Area
- `pipetype`: 0
- **Total length:** 10.0 m
- **dx per cell:** [5.0, 5.0] m
- **Hydraulic diameter:** 1.12838 m

### PUMP 13
- `name`: $13$ int-loop pump
- `ipmpty`: 0

### CONTROL_BLOCK -1
- `name`: unnamed
- `control_type`: ControlTypeSel.Constant
- `cbgain`: 1.0
- `cbxmin`: -1.0E20
- `cbxmax`: 1.0E20
- `cbcon1`: 6.5
- `cbcon2`: 0.0

### SIGNAL_VARIABLE 1
- `name`: unnamed
- `icn1`: 0

### SIGNAL_VARIABLE 2
- `name`: unnamed
- `connection`: 11
- `icn1`: 0

### TRIP 11
