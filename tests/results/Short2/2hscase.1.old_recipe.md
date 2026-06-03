# Reconstruction Prompt: 2hscase.1.old

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("2hscase.1.old")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.

### PIPE 10 ($10$ sg primary tube bundle)

```
add_component(model_id, 'PIPE', 10, {}, initializer={
    "nsegs": 4,
    "n_pipes": 1,
    "length": 4.0,
    "hd": 0.016
})
```

Set properties:
- `epsw` = `1.0E-6`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### PIPE 20 ($20$ sg secondary-side boiler)

```
add_component(model_id, 'PIPE', 20, {}, initializer={
    "nsegs": 3,
    "n_pipes": 1,
    "length": 3.0,
    "hd": 0.006
})
```

Set properties:
- `epsw` = `1.0E-6`
- `calculation_flag` = `CalculationFlag.Area`
- `pipetype` = `0`

### FILL 8 ($8$ primary flow boundary)

```
add_component(model_id, 'FILL', 8, {})
```

Set properties:
- `pin` = `1.55E7`
- `tlin` = `590.0`
- `tvin` = `590.0`
- `flowin` = `5000.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Constant_Mass_Flow`
- `dxin` = `1.0`
- `volin` = `1.0`

### FILL 18 ($18$ secondary fill boundary)

```
add_component(model_id, 'FILL', 18, {})
```

Set properties:
- `pin` = `5.5E6`
- `tlin` = `400.0`
- `tvin` = `400.0`
- `flowin` = `2500.0`
- `alpin` = `0.0`
- `ifty` = `FillIftySel.Constant_Mass_Flow`
- `dxin` = `1.0`
- `volin` = `4.0`

### BREAK 12 ($12$ primary break boundary)

```
add_component(model_id, 'BREAK', 12, {})
```

Set properties:
- `pin` = `1.55E7`
- `tin` = `549.1`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.0`
- `volin` = `1.0`

### BREAK 22 ($22$ secondary break boundary)

```
add_component(model_id, 'BREAK', 22, {})
```

Set properties:
- `pin` = `5.5E6`
- `tin` = `400.0`
- `alpin` = `0.0`
- `isat` = `BreakIsatSel.Enter_liquid_gas_temp`
- `ioff` = `BreakIoffSel.Last_Interp_State_Held_Const`
- `ibty` = `BreakIbtySel.No_Tables`
- `dxin` = `1.0`
- `volin` = `4.0`

### HEAT_STRUCTURE 900 ($900$ upflow sg tube bundle hs)

```
add_component(model_id, 'HEAT_STRUCTURE', 900, {}, initializer={
    "axial": 2,
    "radial": 3,
    "length": 2.0,
    "inner": 8.0E-3,
    "hsycl": "HeatStructureGeometry.CYLINDRICAL",
    "th": 0.0009999999999999992,
    "temp": 549.3,
    "material": "Material 12"
})
```

Set properties:
- `hscyl` = `1`
- `inner_radius` = `8.0E-3`
- `th` = `1.0E-3`
- `hgapo` = `0.0`
- `ichf` = `1`
- `iaxcnd` = `True`
- `nofuelrod` = `HSFuelSel.Not_Fuel_Rod`
- `nfci` = `0`
- `nfcil` = `1`
- `dhtstrz` = `[1.0,1.0]`
- `rftn_table` = `[549.3,549.3,549.3]
[549.3,549.3,549.3]
`

### HEAT_STRUCTURE 910 ($910$ downflow sg tube bundle hs)

```
add_component(model_id, 'HEAT_STRUCTURE', 910, {}, initializer={
    "axial": 2,
    "radial": 3,
    "length": 2.0,
    "inner": 8.0E-3,
    "hsycl": "HeatStructureGeometry.CYLINDRICAL",
    "th": 0.0009999999999999992,
    "temp": 549.3,
    "material": "Material 12"
})
```

Set properties:
- `hscyl` = `1`
- `inner_radius` = `8.0E-3`
- `th` = `1.0E-3`
- `hgapo` = `0.0`
- `ichf` = `1`
- `iaxcnd` = `True`
- `nofuelrod` = `HSFuelSel.Not_Fuel_Rod`
- `nfci` = `0`
- `nfcil` = `1`
- `dhtstrz` = `[1.0,1.0]`
- `rftn_table` = `[549.3,549.3,549.3]
[549.3,549.3,549.3]
`

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
connect_components(model_id, 10, "inlet", "[JUN1] Inlet", 8, 1)
connect_components(model_id, 10, "outlet", "[JUN1] Inlet", 12, 1)
connect_components(model_id, 20, "inlet", "[JUN1] Inlet", 18, 1)
connect_components(model_id, 20, "outlet", "[JUN1] Inlet", 22, 1)
```

## Step 3b — Wire heat structure surfaces to hydraulic components

Use `connect_heat_structure()` for each (hs_cell, face) pair:

**HS 900**

```
connect_heat_structure(model_id, 900, 1, "inner", 10, 1)
connect_heat_structure(model_id, 900, 1, "outer", 20, 1)
connect_heat_structure(model_id, 900, 2, "inner", 10, 2)
connect_heat_structure(model_id, 900, 2, "outer", 20, 2)
```

**HS 910**

```
connect_heat_structure(model_id, 910, 1, "inner", 10, 3)
connect_heat_structure(model_id, 910, 1, "outer", 20, 2)
connect_heat_structure(model_id, 910, 2, "inner", 10, 4)
connect_heat_structure(model_id, 910, 2, "outer", 20, 1)
```


## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
