# Reconstruction Prompt: AdjP

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("AdjP")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 701 (one cell pipe)

```
add_component(model_id, 'PIPE', 701, {}, initializer={
    "nsegs": 2,
    "n_pipes": 1,
    "length": 2.0,
    "hd": 1.0
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### BREAK 201 (side leg one bc)

```
add_component(model_id, 'BREAK', 201, {})
```

Set properties:
- `pin` = `2.0E5`
- `tin` = `600.0`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.Input_Pressure_Table`
- `dxin` = `1.0`
- `volin` = `0.1`

### BREAK 100 (side leg one bc)

```
add_component(model_id, 'BREAK', 100, {})
```

Set properties:
- `pin` = `2.0E5`
- `tin` = `600.0`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.0`
- `volin` = `0.1`

### SIGNAL_VARIABLE 1 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 1, {})
```

Set properties:
- `name` = `unnamed`
- `icn1` = `0`

## Step 3 — Connect components

Use `connect_components()` to wire the hydraulic topology:

```
connect_components(model_id, 701, "inlet", "[JUN1] Inlet", 100, 1)
connect_components(model_id, 701, "outlet", "[JUN1] Inlet", 201, 1)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
