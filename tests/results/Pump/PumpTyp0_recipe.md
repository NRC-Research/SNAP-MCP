# Reconstruction Prompt: PumpTyp0

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #    Simple pump IPMPTY = 0 test.  Closed loop with single PIPE component
#    connected to inlet and outlet of PUMP.  Pump trip is initially off
#    then goes on at 100 seconds.  Stays on to 300 seconds and then goes
#    off.  When trip is off the volumetric flow through the pump is
#    6.5 m^3/s and when the trip is on the volumetric flow through the pump is
#    7 m^3/s.
#

## Step 1 — Create the model

```
create_model("PumpTyp0")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 14 (pipe-to-pump)

```
add_component(model_id, 'PIPE', 14, {}, initializer={
    "nsegs": 2,
    "n_pipes": 1,
    "length": 10.0,
    "hd": 1.12838
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### PUMP 13 ($13$ int-loop pump)

```
add_component(model_id, 'PUMP', 13, {}, initializer={<see schema>})
```

Set properties:
- `name` = `$13$ int-loop pump`
- `ipmpty` = `0`

### CONTROL_BLOCK -1 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -1, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Constant`
- `cbgain` = `1.0`
- `cbxmin` = `-1.0E20`
- `cbxmax` = `1.0E20`
- `cbcon1` = `6.5`
- `cbcon2` = `0.0`

### SIGNAL_VARIABLE 1 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 1, {})
```

Set properties:
- `name` = `unnamed`
- `icn1` = `0`

### TRIP 11 (unnamed)

```
add_component(model_id, 'TRIP', 11, {})
```

## Step 3 — Connect components

Use `connect_components()` for 1-D to 1-D connections, and `connect_pipe_to_vessel()` when the target is a VESSEL:

```
connect_components(model_id, 14, "inlet", "[JUN1] Inlet", 13, 3)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
