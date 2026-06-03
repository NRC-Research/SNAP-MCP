# Reconstruction Prompt: CONTAN1

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #    Base case for some CONTAN test problems.  This is a simple test problem with
#    a FILL-PIPE-BREAK.  It will be used to provide a mass and energy source and sink
#    for a CONTAN component.
#

## Step 1 — Create the model

```
create_model("CONTAN1")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 2 (Primary side PIPE)

```
add_component(model_id, 'PIPE', 2, {}, initializer={
    "nsegs": 12,
    "n_pipes": 1,
    "length": 12.0,
    "hd": 1.0
})
```

Set properties:
- `epsw` = `1.0E-5`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### FILL 1 (channel inlet flow bc)

```
add_component(model_id, 'FILL', 1, {})
```

Set properties:
- `pin` = `1.0E7`
- `tlin` = `584.1`
- `tvin` = `584.1`
- `flowin` = `0.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Mass_FLow_Table`
- `dxin` = `1.0`
- `volin` = `2.0`

### BREAK 3 (channel downstream pressure bc)

```
add_component(model_id, 'BREAK', 3, {})
```

Set properties:
- `pin` = `1.0E5`
- `tin` = `300.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.Opt_4_plus_Solute_Ratio_Table`
- `dxin` = `1.0`
- `volin` = `0.1`

### SIGNAL_VARIABLE 1 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 1, {})
```

Set properties:
- `name` = `unnamed`
- `icn1` = `0`

### TRIP 1001 (unnamed)

```
add_component(model_id, 'TRIP', 1001, {})
```

## Step 3 — Connect components

Use `connect_components()` to wire the hydraulic topology:

```
connect_components(model_id, 2, "inlet", "[JUN1] Inlet", 1, 1)
connect_components(model_id, 2, "outlet", "[JUN1] Inlet", 3, 1)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
