# Reconstruction Prompt: ptpL0br

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("ptpL0br")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 702 (outlet end main leg)

```
add_component(model_id, 'PIPE', 702, {}, initializer={
    "nsegs": 2,
    "n_pipes": 1,
    "length": 5.0,
    "hd": 1.0
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### PIPE 700 (inlet end main leg)

```
add_component(model_id, 'PIPE', 700, {}, initializer={
    "nsegs": 2,
    "n_pipes": 1,
    "length": 3.0,
    "hd": 1.0
})
```

Set properties:
- `epsw` = `0.0`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### FILL 100 (mass flow bc)

```
add_component(model_id, 'FILL', 100, {})
```

Set properties:
- `pin` = `1.0E5`
- `tlin` = `300.0`
- `tvin` = `300.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Constant_Velocity`
- `dxin` = `1.5`
- `volin` = `0.15`

### FILL 101 (mass flow bc)

```
add_component(model_id, 'FILL', 101, {})
```

Set properties:
- `pin` = `1.0E5`
- `tlin` = `370.0`
- `tvin` = `370.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Constant_Velocity`
- `dxin` = `0.5`
- `volin` = `0.1`

### BREAK 201 (side leg one bc)

```
add_component(model_id, 'BREAK', 201, {})
```

Set properties:
- `pin` = `1.0E5`
- `tin` = `300.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `2.5`
- `volin` = `0.75`

### TEE 701 (the tee)

```
add_component(model_id, 'TEE', 701, {})
```

Set properties:
- `name` = `the tee`

## Step 3 — Connect components

Use `connect_components()` to wire the hydraulic topology:

```
connect_components(model_id, 702, "inlet", "[JUN1] Inlet", 701, 1)
connect_components(model_id, 702, "outlet", "[JUN1] Inlet", 201, 1)
connect_components(model_id, 700, "inlet", "[JUN1] Inlet", 100, 1)
connect_components(model_id, 700, "outlet", "[JUN2] Inlet", 701, 1)
connect_components(model_id, 101, "inlet", "[JUN1] Inlet", 701, 5)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
