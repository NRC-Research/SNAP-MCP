# Reconstruction Prompt: 1valv-SD-BC-Pcte

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("1valv-SD-BC-Pcte")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### BREAK 1 (Linea de vapor)

```
add_component(model_id, 'BREAK', 1, {})
```

Set properties:
- `pin` = `6.6E6`
- `tin` = `547.204`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Set_liquid_and_gas_to_Tsat`
- `ioff` = `BreakIoffSel.Define_the_Initial_State`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `0.1`
- `volin` = `1.0E5`

### BREAK 101 (Linea de vapor)

```
add_component(model_id, 'BREAK', 101, {})
```

Set properties:
- `pin` = `1.0E5`
- `tin` = `372.756`
- `alpin` = `1.0`
- `isat` = `BreakIsatSel.Set_liquid_and_gas_to_Tsat`
- `ioff` = `BreakIoffSel.Define_the_Initial_State`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `0.1`
- `volin` = `1.0E5`

### VALVE 21 (Valvula SD 538)

```
add_component(model_id, 'VALVE', 21, {}, initializer={<see schema>})
```

Set properties:
- `name` = `Valvula SD 538`

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
connect_components(model_id, 1, "inlet", "[JUN1] Inlet", 21, 1)
connect_components(model_id, 101, "inlet", "[JUN1] Inlet", 21, 3)
```

## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
