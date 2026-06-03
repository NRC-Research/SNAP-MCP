# Reconstruction Prompt: BreakEnthalpy

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("BreakEnthalpy")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 2 (inlet pipe)

```
add_component(model_id, 'PIPE', 2, {}, initializer={
    "nsegs": 1,
    "n_pipes": 1,
    "length": 8.2913,
    "hd": 0.04625
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### PIPE 3 (heater u-tube bank)

```
add_component(model_id, 'PIPE', 3, {}, initializer={
    "nsegs": 8,
    "n_pipes": 1,
    "length": 66.3304,
    "hd": 0.04625
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### PIPE 4 (outlet pipe)

```
add_component(model_id, 'PIPE', 4, {}, initializer={
    "nsegs": 1,
    "n_pipes": 1,
    "length": 8.2913,
    "hd": 0.04625
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### FILL 5 (fw outlet bc)

```
add_component(model_id, 'FILL', 5, {})
```

Set properties:
- `pin` = `410.0`
- `tlin` = `342.7`
- `tvin` = `342.7`
- `flowin` = `7936.64`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Constant_Mass_Flow`
- `dxin` = `8.2913`
- `volin` = `0.013929`

### BREAK 1 (fw inlet bc)

```
add_component(model_id, 'BREAK', 1, {})
```

Set properties:
- `pin` = `410.0`
- `tin` = `342.7`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `8.2913`
- `volin` = `0.013929`

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
connect_components(model_id, 2, "inlet", "[JUN1] Inlet", 1, 1)
connect_components(model_id, 2, "outlet", "[JUN1] Inlet", 3, 1)
connect_components(model_id, 3, "outlet", "[JUN1] Inlet", 4, 1)
connect_components(model_id, 4, "outlet", "[JUN1] Inlet", 5, 1)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
