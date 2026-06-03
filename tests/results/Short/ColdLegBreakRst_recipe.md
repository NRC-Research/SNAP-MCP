# Reconstruction Prompt: ColdLegBreakRst

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

## Step 1 — Create the model

```
create_model("ColdLegBreakRst")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.


## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
