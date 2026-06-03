# Reconstruction Prompt: PumpTyp0_Rev1

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #    Same as test problem PumpTyp0, except NPMPSD was changed from -1 to 2.
#    Signal variable 2 is trip status for trip 11.
#    Trip 11 is initially off, then goes on at 100 secs and then off again at 300 secs.
#

## Step 1 — Create the model

```
create_model("PumpTyp0_Rev1")
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

### SIGNAL_VARIABLE 2 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 2, {})
```

Set properties:
- `name` = `unnamed`
- `connection` = `11`
- `icn1` = `0`

### TRIP 11 (unnamed)

```
add_component(model_id, 'TRIP', 11, {})
```

## Step 3 — Connect components

Use `connect_components()` to wire the hydraulic topology:

```
connect_components(model_id, 14, "inlet", "[JUN1] Inlet", 13, 3)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
