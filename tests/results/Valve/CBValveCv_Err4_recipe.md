# Reconstruction Prompt: CBValveCv_Err4

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("CBValveCv_Err4")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### BREAK 436 (inlet)

```
add_component(model_id, 'BREAK', 436, {})
```

Set properties:
- `pin` = `1.2E6`
- `tin` = `300.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Use_separate_tables_or_CS`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.Opt_3_plus_NC_Gas_PP_Table`
- `dxin` = `0.3`
- `volin` = `0.09`

### BREAK 666 (exit)

```
add_component(model_id, 'BREAK', 666, {})
```

Set properties:
- `pin` = `1.0E6`
- `tin` = `300.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Use_separate_tables_or_CS`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.Opt_3_plus_NC_Gas_PP_Table`
- `dxin` = `0.3`
- `volin` = `0.09`

### VALVE 515 (chk vlv)

```
add_component(model_id, 'VALVE', 515, {}, initializer={<see schema>})
```

Set properties:
- `name` = `chk vlv`

### CONTROL_BLOCK -329 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -329, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Sum`
- `cbgain` = `1.0`
- `cbxmin` = `-1.0E20`
- `cbxmax` = `1.0E20`
- `cbcon1` = `0.0`
- `cbcon2` = `0.0`

### CONTROL_BLOCK -331 (unnamed)

```
add_component(model_id, 'CONTROL_BLOCK', -331, {})
```

Set properties:
- `name` = `unnamed`
- `control_type` = `ControlTypeSel.Function`
- `cbgain` = `1.0`
- `cbxmin` = `-1.0E20`
- `cbxmax` = `1.0E20`
- `cbcon1` = `0.0`
- `cbcon2` = `0.0`

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
connect_components(model_id, 436, "inlet", "[JUN1] Inlet", 515, 1)
connect_components(model_id, 666, "inlet", "[JUN1] Inlet", 515, 3)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
