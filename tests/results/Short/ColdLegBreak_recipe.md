# Reconstruction Prompt: ColdLegBreak

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("ColdLegBreak")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### BREAK 25 ($25$ cold leg left BC)

```
add_component(model_id, 'BREAK', 25, {})
```

Set properties:
- `pin` = `5.91E6`
- `tin` = `547.8`
- `alpin` = `0.5`
- `isat` = `BreakIsatSel.Set_liquid_and_gas_to_Tsat`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.1033`
- `volin` = `0.42278`

### BREAK 30 ($30$ cold leg right BC)

```
add_component(model_id, 'BREAK', 30, {})
```

Set properties:
- `pin` = `5.91E6`
- `tin` = `547.8`
- `alpin` = `0.5`
- `isat` = `BreakIsatSel.Set_liquid_and_gas_to_Tsat`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.1033`
- `volin` = `0.42278`

### BREAK 229 ($229$ small break pressure boundary)

```
add_component(model_id, 'BREAK', 229, {})
```

Set properties:
- `pin` = `1.0135E5`
- `tin` = `373.2`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Define_the_Initial_State`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `0.06668`
- `volin` = `4.0348E-4`

### TEE 29 ($29$ cold leg section 2c)

```
add_component(model_id, 'TEE', 29, {})
```

Set properties:
- `name` = `$29$ cold leg section 2c`

### SIGNAL_VARIABLE 1 (unnamed)

```
add_component(model_id, 'SIGNAL_VARIABLE', 1, {})
```

Set properties:
- `name` = `unnamed`
- `icn1` = `0`

### TRIP 1 (unnamed)

```
add_component(model_id, 'TRIP', 1, {})
```

## Step 3 — Connect components

Use `connect_components()` for 1-D to 1-D connections, and `connect_pipe_to_vessel()` when the target is a VESSEL:

```
connect_components(model_id, 25, "inlet", "[JUN1] Inlet", 29, 1)
connect_components(model_id, 30, "inlet", "[JUN1] Inlet", 29, 3)
connect_components(model_id, 229, "inlet", "[JUN1] Inlet", 29, 5)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
