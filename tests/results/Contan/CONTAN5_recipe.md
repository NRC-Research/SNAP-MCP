# Reconstruction Prompt: CONTAN5

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #    Same as test problem CONTAN4, except added legacycontm = .false. to namelist input
#    and added the addition input required for the CONTAN component.
#

## Step 1 — Create the model

```
create_model("CONTAN5")
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
- `ibty` = `BreakIbtySel.CONTAN_Component`
- `dxin` = `1.0`
- `volin` = `0.1`

### CONTROL_BLOCK -1 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -1, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Multiply`
- `cbgain` = `1.0`
- `cbxmin` = `0.0`
- `cbxmax` = `1.0E30`
- `cbcon1` = `0.0`
- `cbcon2` = `0.0`

### CONTROL_BLOCK -2 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -2, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Integrate`
- `cbgain` = `1.0`
- `cbxmin` = `0.0`
- `cbxmax` = `1.0E30`
- `cbcon1` = `0.0`
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
- `icn1` = `0`

### SIGNAL_VARIABLE 3 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 3, {})
```

Set properties:
- `name` = `unnamed`
- `icn1` = `0`

### TRIP 1001 (unnamed)

```
add_component(model_id, 'TRIP', 1001, {})
```

### CONTAN_COMPARTMENT 103 (unnamed)

```
add_component(model_id, 'CONTAN_COMPARTMENT', 103, {})
```

Set properties:
- `name` = `unnamed`
- `rml` = `1000.0`
- `itrkl` = `OnOffSel.On`

## Step 3 — Connect components

Use `connect_components()` for 1-D to 1-D connections, and `connect_pipe_to_vessel()` when the target is a VESSEL:

```
connect_components(model_id, 2, "inlet", "[JUN1] Inlet", 1, 1)
connect_components(model_id, 2, "outlet", "[JUN1] Inlet", 3, 1)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
