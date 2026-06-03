# Model Summary: PumpTyp0
**Purpose:** #    Simple pump IPMPTY = 0 test.  Closed loop with single PIPE component
#    connected to inlet and outlet of PUMP.  Pump trip is initially off
#    then goes on at 100 seconds.  Stays on to 300 seconds and then goes
#    off.  When trip is off the volumetric flow through the pump is
#    6.5 m^3/s and when the trip is on the volumetric flow through the pump is
#    7 m^3/s.
#

## Components

| Type | CC# | Name |
|---|---|---|
| PIPE | 14 | pipe-to-pump |
| PUMP | 13 | $13$ int-loop pump |
| CONTROL_BLOCK | -1 | unnamed |
| SIGNAL_VARIABLE | 1 | unnamed |
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

### TRIP 11
