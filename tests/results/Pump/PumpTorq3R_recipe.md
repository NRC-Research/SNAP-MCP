# Reconstruction Prompt: PumpTorq3R

Use the snap-trace MCP tools to recreate the following TRACE model.
Call `snap_status()` first to confirm the connection, then follow the steps below.

**Model purpose:** #     pump motor torque test problem - IPMPTY = 3.
#     Restarts from PumpTorq3 at time zero.  If time zero restart
#     dump is good then PumpTorq3 and PumpTorq3R should be the same.
#

## Step 1 — Create the model

```
create_model("PumpTorq3R")
```

## Step 2 — Add components

Add the following components with `add_component()`. Consult `get_component_schema(type)` before each call.


## Step 4 — Validate and export

```
validate_model(model_id)
export_trcin(model_id)
```
