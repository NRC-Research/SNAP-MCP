# Reconstruction Prompt: CCTF_ColdLeg

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("CCTF_ColdLeg")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 21 (Cold Leg)

```
add_component(model_id, 'PIPE', 21, {}, initializer={
    "nsegs": 5,
    "n_pipes": 1,
    "length": 4.1719,
    "hd": 0.1552
})
```

Set properties:
- `epsw` = `5.0E-6`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### FILL 11 (steam fill)

```
add_component(model_id, 'FILL', 11, {})
```

Set properties:
- `pin` = `2.45E5`
- `tlin` = `399.9`
- `tvin` = `405.0`
- `flowin` = `0.688`
- `alpin` = `1.0`
- `ifty` = `FillIftySel.Mass_FLow_Table`
- `dxin` = `1.0`
- `volin` = `0.01892`

### FILL 12 (water fill)

```
add_component(model_id, 'FILL', 12, {})
```

Set properties:
- `pin` = `2.45E5`
- `tlin` = `309.2`
- `tvin` = `399.9`
- `flowin` = `0.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Mass_FLow_Table`
- `dxin` = `1.0`
- `volin` = `1.735E-3`

### BREAK 31 (Press BC)

```
add_component(model_id, 'BREAK', 31, {})
```

Set properties:
- `pin` = `2.45E5`
- `tin` = `405.0`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Define_the_Initial_State`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.0`
- `volin` = `0.01892`

### SIGNAL_VARIABLE 1 (time)

```
add_component(model_id, 'SIGNAL_VARIABLE', 1, {})
```

Set properties:
- `name` = `time`
- `icn1` = `0`

## Step 3 — Connect components

Use `connect_components()` to wire the hydraulic topology:

```
connect_components(model_id, 21, "inlet", "[JUN1] Inlet", 11, 1)
connect_components(model_id, 21, "outlet", "[JUN1] Inlet", 31, 1)
# FILL 12 inlet → ('Crossflow', 21, 2, 45.0)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
