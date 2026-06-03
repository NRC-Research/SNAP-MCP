# Reconstruction Prompt: PumpTorq3

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #     pump motor torque test problem - IPMPTY = 3.
#     This test is identical to PumpTorq2 with the added feature
#     that IPMPTR points to trip 1.  Initial motor torque will be
#     1000 N-m before trip and then 500 N-m after trip.
#

## Step 1 — Create the model

```
create_model("PumpTorq3")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### BREAK 702 (bottom break)

```
add_component(model_id, 'BREAK', 702, {})
```

Set properties:
- `pin` = `1.0E6`
- `tin` = `373.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `0.3`
- `volin` = `0.09`

### BREAK 701 (bottom break)

```
add_component(model_id, 'BREAK', 701, {})
```

Set properties:
- `pin` = `1.0E6`
- `tin` = `373.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `0.3`
- `volin` = `0.09`

### PUMP 700 (pump no. 2)

```
add_component(model_id, 'PUMP', 700, {}, initializer={<see schema>})
```

Set properties:
- `name` = `pump no. 2`
- `ipmpty` = `3`

### CONTROL_BLOCK -680 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -680, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Constant`
- `cbgain` = `1.0`
- `cbxmin` = `-1.0E4`
- `cbxmax` = `1.0E4`
- `cbcon1` = `500.0`
- `cbcon2` = `1000.0`

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
- `connection` = `700`
- `icn1` = `0`

### SIGNAL_VARIABLE 3 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 3, {})
```

Set properties:
- `name` = `unnamed`
- `connection` = `700`
- `icn1` = `0`

### TRIP 1 (unnamed)

```
add_component(model_id, 'TRIP', 1, {})
```

## Step 3 — Connect components

Use `connect_components()` for 1-D to 1-D connections, and `connect_pipe_to_vessel()` when the target is a VESSEL:

```
connect_components(model_id, 702, "inlet", "[JUN1] Inlet", 700, 3)
connect_components(model_id, 701, "inlet", "[JUN1] Inlet", 700, 1)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
