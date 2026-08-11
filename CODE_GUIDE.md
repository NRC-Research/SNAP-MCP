# SNAP-MCP Code Guide

Developer reference for the SNAP-MCP codebase.

---

## Architecture overview

```
mcp_server.py               ← entry point; wires FastMCP + all modules
snap_trace/
  snap_env.py               ← SNAP bootstrap, py4j / MEBatch startup
  session.py                ← model registry (SQLite + in-memory cache)
  component_map.py          ← TRACE component type → SNAP API method map
  type_converter.py         ← enum string + value conversion
  resources.py              ← MCP resources (static reference content)
  tools/
    model_tools.py          ← snap_status, create_model, open_med, import_trcin, list_models
    component_tools.py      ← add_component, set_component_property, list_components, get_component, get_component_schema
    connection_tools.py     ← connect_components, get_connections
    export_tools.py         ← export_trcin, save_med, validate_model
```

The MCP framework used is **FastMCP** (`mcp[cli]>=1.0`). Each tool module exposes a `register(mcp)` function that decorates its tools with `@mcp.tool()`. Resources follow the same pattern in `resources.py`.

Transport is **stdio** only — Claude Code (and Claude Desktop) connect via subprocess stdin/stdout.

---

## mcp_server.py

Entry point. Three responsibilities:

1. **Save real stdout** (`_real_stdout = sys.stdout`) before any SNAP import. SNAP's `snap.streams` module replaces `sys.stdout` with a `_StreamLogHandler` when `snap.model_editor` is imported. MCP's stdio transport later calls `sys.stdout.buffer` and crashes if stdout has been replaced. Restoring it at the top of `main()` before `mcp.run()` fixes this.

2. **Trigger MEBatch startup** by importing `snap_trace.snap_env` (side-effectful). This starts the background thread immediately so the first tool call doesn't have to wait.

3. **Register all tools and resources** by calling each module's `register(mcp)`.

FastMCP constructor note: as of MCP v1.27.1, the description kwarg is `instructions`, not `description`.

---

## snap_env.py

Bootstraps the SNAP Python path and starts MEBatch.

- Inserts `SNAP_PYTHON_PATH` at the front of `sys.path` so `snap.*` imports resolve.
- Fires a daemon thread (`snap-init`) that calls `snap.model_editor.find_plugin("TRACE")`, which triggers the py4j handshake with the MEBatch JVM process.
- Exposes `status()` → dict and `wait_ready(timeout)` used by tools that require SNAP to be up before proceeding.

The thread is daemon so it doesn't prevent process exit if SNAP fails to start.

**Tools wait for startup rather than refusing it.** A tool called before SNAP is ready parks on the
init thread for up to `SNAP_MCP_STARTUP_WAIT` (default 90 s) and raises only if startup genuinely
never completes. An earlier design failed fast and told the caller to poll `snap_status()` and
retry, which an LLM agent cannot act on — it has no clock and no sleep, so it burns turns polling.
Waiting is also no less safe than refusing: a parked call is blocked on an event, so it cannot
reach the gateway or trip `reset()` mid-initialization, and unlike a refusal it does not come
straight back as a retry.

**Gateway access is serialized.** A single `_GATEWAY_LOCK` serializes all tool calls, because the
Py4J socket is not thread-safe and FastMCP runs synchronous tools on a thread pool. Concurrent
calls without it corrupt the connection rather than merely racing.

**Recovery relaunches MEBatch in-process.** On a genuine break, `reset()` kills the old JVM once,
shuts down SNAP's `__MODEL_EDITOR__` singleton, and `find_plugin` relaunches MEBatch in the same
process; `get_model()` then reloads each model from its autosaved `.med`, so a caller's `model_id`
survives the restart. Do not kill an in-flight relaunch and do not evict the `snap`/`py4j` modules
from `sys.modules` to force a clean import — both wedge the process.

The server also logs to `~/.snap_trace/server.log`, recording the real exception plus the tool name
and arguments whenever a gateway break is detected. That log is the fastest way to distinguish a
true break from a misclassified Java error.

---

## session.py

Maintains two parallel stores for `TraceModel` objects:

- **In-memory dict** (`_models: dict[str, TraceModel]`) — fast access during a session.
- **SQLite database** (`~/.snap_trace/models.db`) — survives restarts; maps `model_id → med_path`.

`model_id` is an 8-character hex string from `uuid4`. Models are stored on disk as `.med` files under `~/.snap_trace/models/`.

**autosave** is called by every mutating tool after making changes. It writes the current in-memory model object back to its `.med` file. On the next server start, `get_model()` reloads from disk if the model is not in `_models`.

Key functions:

| Function | What it does |
|----------|-------------|
| `create_model(name, version)` | Creates a new TraceModel via `trace.new_model()`, saves to disk, registers in DB |
| `register_model(name, model, source_path)` | Registers a model already opened from a file (used by `open_med_model` and `import_trcin`) |
| `get_model(model_id)` | Returns from cache or reloads from `.med` if not cached |
| `autosave(model_id)` | Writes in-memory model to its `.med` path |
| `list_models()` | Returns all rows from the SQLite models table |

---

## component_map.py

`COMPONENT_MAP` is the single source of truth mapping MCP component type strings (e.g. `"PIPE"`) to the SNAP Python API. Each entry has four fields:

| Field | Purpose |
|-------|---------|
| `create` | `TraceModel` method name for creation (e.g. `"create_pipe"`) |
| `list` | `TraceModel` method that returns all components of this type (e.g. `"pipes"`) |
| `initializer` | Category string passed to `model.component_initializer()`, or `None` |
| `first_arg` | Property key whose value becomes the first positional arg to the create method (used by `CONTROL_BLOCK` and `SIGNAL_VARIABLE`) |

Three utility functions use this map:

- **`create_component`** — factory: resolves the create method, builds an initializer if needed, calls the create method with the right argument order, then applies all properties. Enum properties are applied before scalar properties because SNAP requires the type selector to be set before dependent fields (e.g. `FILL.ifty` before `FILL.flowin`).

- **`find_component`** — scans every `list` method on the model to find a component by CC number. Returns `(comp_type_str, component)`.

- **`iter_all_components`** — yields `(comp_type, component)` for every component in the model, used by `list_components` and `get_connections`.

One subtlety: SNAP's list methods sometimes return a single object instead of a list when there is only one component. `_coerce_list()` normalizes this.

---

## type_converter.py

Converts values from the JSON/AI representation to what the SNAP Python API expects.

**`resolve_enum(value: str)`** — parses `"ClassName.MethodName"` strings, looks up the class in `snap.codes.trace.enums`, and calls the method to get the enum instance. Returns `None` if the string isn't a valid enum reference.

**`convert(value)`** — applies `resolve_enum` first, then handles `"true"`/`"false"` strings.

**`set_property(comp, name, value)`** — the main entry point for property assignment:
- If `value` is a list-of-lists: treats it as a table and calls `.read([...])` on each row of the named attribute. This is how `initial_conditions_cell_table` and `friction_edge_table` are populated.
- If `value` is a flat list: converts each element and sets the attribute directly.
- Otherwise: converts and calls `setattr`.

Dot-path traversal one level deep (e.g. `"fluid_segment.friction_edge_table"`) is handled in `component_tools.py:set_component_property`, not here.

---

## tools/model_tools.py

Thin wrappers around `snap_env` and `session`. All tools that need SNAP running call `snap_env.wait_ready()` before proceeding. `open_med_model` and `import_trcin` use SNAP's `trace.open_model()` and `trace.import_ascii()` then hand off to `session.register_model()`.

`list_models` is **summary-first**: the registry is append-only and never pruned, so a long-lived
install accumulates hundreds of rows and returning all of them buries the caller. It returns the 20
newest with a true `total`, plus `limit`, `name_contains`, and `detail='full'` for the cases that
need more.

`path` is accepted as an alias for `med_file_path` and `trcin_path`. Callers guess `path` almost
every time, and without the alias the validation error names a field the caller never used, which
reads as a broken tool rather than a wrong argument name.

---

## tools/component_tools.py

Most complex tool module. Key points:

- `get_component_schema` returns a hardcoded dict per component type. Adding a new type requires updating both `COMPONENT_MAP` and the `schemas` dict here.
- `add_component` delegates entirely to `component_map.create_component`, then calls `session.autosave`.
- `get_component` reflects all non-callable, non-private attributes. This is a best-effort inspector; some SNAP proxy attributes may throw on access and are silently skipped. For `HEAT_STRUCTURE` components, `_extract_mesh_info` is called after the flat scan and its result is returned as a top-level `radial_mesh` key.

**`_extract_mesh_info(comp)`** walks `comp.mesh.material_regions` and returns a dict with a `layers` list. Each layer entry contains:

| Field | Source |
|-------|--------|
| `material` | `str(region.material)` — see quirk below |
| `thickness_m` | `float(region.thickness)` |
| `meshpoints` | `[float(p) for p in region.meshpoints]` — normalized radial coordinates (0–1) |

All field accesses are individually try/caught so a failure on one field doesn't suppress the others.

---

## tools/connection_tools.py

`connect_components` does a single `setattr(comp, face, (slot, target_cc, cell))` — directly mirroring the SNAP Python API pattern from the standpipe example. The tuple assignment is how SNAP wires junctions.

**The slot is resolved automatically.** The junction slot belongs to the *target*, not the source —
a distinction callers get wrong almost every time, producing a loop of `InvalidFaceException`.
`connect_components` now derives it: BREAK/FILL → `[JUN1] Inlet`, pipe → the free end. A wrong or
blank value is corrected rather than rejected, and the correction is reported back in `slot_note`.
A target with no free junction returns an actionable message ("a pipe cannot connect both ends to
the same target…") instead of a raw Py4J trace.

**VESSEL connection quirk:** `connect_components` does NOT work for VESSEL targets. The Java `setMultiJunctionConnection` method does strict string matching on face labels and throws `RuntimeException` for `"[JUN1] Inlet"` when the target is a `VesselComponent`. Use `connect_pipe_to_vessel` instead.

`connect_pipe_to_vessel` converts (level, ring, sector) coordinates to the flat cell index `(level-1)*(nr*nt) + (ring-1)*nt + (sector-1) + 1` and calls `setattr(hydro_comp, pipe_face, (vessel_face, vessel_cc, flat_cell))`. Valid `vessel_face` strings for cylindrical geometry: `"Positive Azimuthal"`, `"Negative Azimuthal"`, `"Positive Radial"`, `"Negative Radial"`. Axial faces are excluded by the SNAP API for external connections.

`get_connections` iterates all components and tries `getattr(comp, face)` for `inlet`, `outlet`, and `side`. Non-existent faces return `None` and are skipped.

---

## tools/export_tools.py

`export_trcin`:
- Calls `model.export(path)`. SNAP writes the file synchronously and then returns an export result set.
- The result set's `.iterator()` call raises a `Py4JError` due to Java module access restrictions — this is benign (the file is already written). The exception is caught and ignored.
- Reads the written file back as a string and returns it.
- If no `output_path` is given, uses `tempfile.mkstemp` and deletes it after reading.

`validate_model`:
- Calls `model.export(tmp_path, check=True)`.
- SNAP raises on hard errors; soft warnings still produce a file. The exception message is inspected for `"warning"` to distinguish the two cases.

---

## resources.py

Five `@mcp.resource(uri)` functions returning static strings. They exist so an AI assistant can reference workflow steps, enum values, connection syntax, and example code without needing tool calls.

`trace://example/standpipe` reads `~/run-snap500/Samples/TRACE/Standpipe/standpipe.py` at request time. All others return inline strings.

---

## tools/component_tools.py — set_vessel_table

VESSEL per-cell initial conditions (pressure, temperatures, void fraction) and edge hydraulic diameters are stored in `Hydro3DPropertyTable` objects. These are NOT reachable via `set_component_property`'s dot-path traversal. `set_vessel_table` accesses them directly.

Table accessor pattern:
- **Cell tables** (no axis arg): `vessel.p_table`, `vessel.tl_table`, `vessel.tv_table`, `vessel.alp_table`, `vessel.pa_table`, `vessel.s_table`
- **Edge tables** (take `AxisSel` enum): `vessel.hd_table(AxisSel.AXIAL())`, `vessel.hd_table(AxisSel.AZIMUTHAL())`, `vessel.hd_table(AxisSel.RADIAL())`, and similarly for `frac_table`, `kfac_table`, `vv_table`, `vl_table`
- `AxisSel` is in `snap.codes.trace.enums`. `AxisSel.AXIAL()` is a factory method — must be called.

`Hydro3DPropertyTable` interface: `table.row_count` = nz (axial levels), `table.column_count` = nr×nt (planar cells per level). Set via `table[row_idx] = [v1, v2, ...]` (0-based row index).

Broadcasting in `_broadcast_vessel_value`: float → uniform; `list[float]` of length nz → per-level; `list[list[float]]` of shape nz×(nr×nt) → full grid.

---

## Known quirks and gotchas

| Issue | Detail |
|-------|--------|
| `sys.stdout` hijack | `snap.streams` replaces `sys.stdout` on import. Fixed in `mcp_server.py` by saving/restoring around `mcp.run()`. |
| `model.breaks()` coercion | SNAP returns a bare object (not a list) when there is exactly one break. `_coerce_list()` in `component_map.py` handles this. |
| Enum factory methods need `()` | `BreakIbtySel.No_Tables` is a method, not a constant — it must be called. `type_converter.py` calls it automatically when given `"BreakIbtySel.No_Tables"`. |
| Py4JError on export | `model.export()` raises after writing the file. Caught and ignored in `export_tools.py`. |
| FastMCP v1.27.1 API | Constructor arg is `instructions`, not `description`. |
| Enum ordering in `create_component` | Enum-valued properties are applied before scalars because SNAP gates some scalar fields on the enum selector being set first. |
| `ComponentReference.name` inaccessible | `mesh.material_regions[i].material` returns a `ComponentReference` proxy whose `.name` attribute raises. Use `str(region.material)` instead — it returns the material name string directly (e.g. `"Material 8"`). |
| `HEAT_STRUCTURE` mesh is not a flat property | `comp.mesh` returns a nested `MeshpointTable` object that `str()` renders as `""`. The flat-property scan in `get_component` cannot see it; `_extract_mesh_info` handles it explicitly. |
| `fluid_segment` setter is broken in SNAP API | The `fluid_segment.setter` on PIPE (run-snap500 version) has an `if/elif` chain that leaves `java_value` unbound when passed a plain string. Setting it via MCP always fails. Do not include `fluid_segment` in `add_component` properties or `set_component_property` calls — it is a display label only and does not affect physics. Excluded from prompt generation in `run_tests.py`. |
| `add_component` property failures are non-fatal | A failing property (e.g. `fluid_segment`) no longer aborts the whole call. `create_component` now collects failures and returns them as `warnings` in the result. All other properties in the dict are still applied. |
| `rftn_table` is a `TemperatureTable`, not a row-based table | The old `set_property` code called `table[i].read(row)` for list-of-lists values, which works for some table types but not `rftn_table` — its rows are `PropertyValueList` objects (no `.read()`). Fixed in `type_converter.py`: now calls `table.read(rows)` on the table itself, with fallback to `table[i] = row`. |
| HS-to-fluid coupling requires `connect_heat_structure` | `cells[i].inner.hcom.reference` is three levels deep; `set_component_property` dot-path only traverses one level. Use the dedicated `connect_heat_structure` tool instead. |
| HS-to-VESSEL coupling broken via `hcom.reference` | `setReferencedCellID(cc*1000+flat_cell)` is decoded by `CellReconnector` as `(within_level_0based, axial_0based)` — not a flat sequential index — causing `ArrayIndexOutOfBoundsException`. For VESSEL targets, call `setHydroRef`/`setCellRef` directly on `surface.hcom.java_object`: `vessel_j.getCellAt(flat_0based)` uses the single-arg overload which correctly computes `level = flat // (nr*nt)`, `within = flat % (nr*nt)`. The packed-integer read-back (`getReferencedCellID`) also overflows 32-bit `int` for vessel cells and cannot be round-tripped. |
| SNAP plugin 4.7.0 vs TRACE 5.0p9 FILL SV card mismatch | SNAP plugin 4.7.0 exports a 5-field signal-variable card for FILL components (`ifmlsv ifmvsv iftlsv iftvsv ifasv`) but TRACE 5.0 Patch 9 on the target development host expects the older 4-field layout (`ifmmsv iftlsv iftvsv ifasv`). The extra field shifts all subsequent cards by one token and causes a cascading parse failure. Fixed in `export_trcin` via `_fixup_trcin()` which collapses the 5-field layout to 4-field on export. **Prefer `save_med` over `export_trcin` for model handoff — `.med` is version-independent.** |
| Integer-flag fields exported as floats | SNAP stores some integer-type FILL fields (e.g. `falk`) as Java `double` internally; Py4J prints them as `0.0`, `1.0` etc. in the ASCII export. The TRACE parser rejects these for integer-only fields. Fixed in `export_trcin` via `_fixup_trcin()` which replaces `N.0` tokens with `N`. |
| `.inp` files are TRACE-version sensitive | SNAP's `model.export()` always writes the TRCIN format for the TRACE version the plugin was built against. Importing a SNAP-exported `.inp` into a different TRACE plugin version will fail with card-format errors. Use `save_med` + `validate_model` as the primary model artifact; only call `export_trcin` when preparing an actual TRACE run. |
| Blank junction label maps to `[JUN1] Inlet` | When the raw connection data shows `('', cc, cell)`, the SNAP face name is actually `[JUN1] Inlet`. `connect_components` must use `[JUN1] Inlet`, not `""`. |
| `FILL.name` has no setter | Setting `name` on a `Fill` object raises "property 'name' of 'Fill' object has no setter". Do not include `name` in `add_component` properties for FILL components. |
| `HEAT_STRUCTURE.nfax` is a per-cell array | `nfax` (fine mesh nodes per axial cell) cannot be set as a scalar integer — SNAP stores it as an array indexed per cell. Setting it via `add_component` fails with `'int' object is not subscriptable`. Use `set_component_property` with a list (e.g. `[3, 3, 3, 3]` for 4 axial cells) after creation. |
| A Java error is not a dead gateway | Every `Py4JJavaError` traceback contains the frame `at py4j.GatewayConnection.run`. Substring-matching `"GatewayConnection"` to detect a broken connection therefore fires on *routine* modeling errors — a bad `connect_components` argument would reset a perfectly healthy gateway. Only true network failures count: `Py4JNetworkError`, connection refused, broken pipe. |
| `"TRACE already loaded"` in the MEBatch log is benign | It appears on every launch and is not evidence of a failed or duplicated start. |
| Never `pkill -f MEBatch` | The JVM is multi-tenant — several MCP clients can be running their own MEBatch under the same account. Blanket-killing by name takes out other tenants' sessions. Startup and `reset()` reap orphans and own-process JVMs only. |
| The TRACE plugin jar is signed | A modified or rebuilt jar fails to load: TRACE reports `PluginNotFound: 'TRACE'` and `snap_status` stays `ready:false`. Do not patch the jar — use the Py4J reflection path this server already uses. Keep a pristine copy of the vendor jar alongside the installed one so the original can be restored without a reinstall. |
| An unreadable jar looks like a plugin bug | If the account running SNAP cannot read the jar, the symptom is `plugin_version: null` rather than a permission error — easy to misdiagnose. Check file permissions before suspecting the plugin. |
| Wrong `SNAP_PYTHON_PATH` surfaces as a missing attribute | Pointing at a SNAP install whose TRACE plugin predates `new_model` fails at `create_model` with `module 'snap.codes.trace' has no attribute 'new_model'`. It is a version mismatch, not a bug — point at an install with TRACE 4.7.0 or newer. |
| Optional tool parameters must be declared `T \| None` | Writing `list[str] = None` or `int = None` makes the generated schema advertise a non-null type with a `null` default. Strict MCP clients reject the tool outright. Always spell optional parameters `list[str] \| None = None`. |
| A one-shot pipe test exits 1 on a healthy server | `printf ... \| server` exits 1 with `server is closing: EOF`. That is normal for MCP servers when stdin closes, and is not evidence the server is broken. |

---

## Adding a new component type

1. Add an entry to `COMPONENT_MAP` in `component_map.py` with `create`, `list`, `initializer`, and `first_arg`.
2. Add a `schemas[TYPE]` entry in `component_tools.py:get_component_schema` with `description`, `initializer_fields`, `key_properties`, and `connection_slots`.
3. If the type belongs to a new category, add it to the category dict in `resources.py:component_types`.

---

## Configuration

The server reads three environment variables at startup. For Claude Code, set them via `claude mcp add -e KEY=VALUE` — the registration is stored in `~/.claude.json`. For Claude Desktop, set them in the `env` block of `~/Library/Application Support/Claude/claude_desktop_config.json`.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SNAP_PYTHON_PATH` | `~/run-snap500/python` | Path to SNAP's Python API directory |
| `SNAP_TRACE_DB` | `~/.snap_trace/models.db` | SQLite model registry |
| `SNAP_TRACE_WORKDIR` | `~/.snap_trace/models/` | Working .med file storage |
| `SNAP_TRACE_TARGET_VERSION` | `V5.0p9` | TRACE binary version being exported for; controls which `_fixup_trcin` patches are applied and the default version used in `create_model` |
| `SNAP_MCP_STARTUP_WAIT` | `90` | Seconds a tool call will wait for MEBatch startup before raising |

---

## Notes for agent-driven use

This server is built to be driven by an LLM agent, and two properties of that setting shape the
design more than raw tool speed does.

**Response size is the cost driver, not tool latency.** Wall-clock time for an agent turn tracks
the number of tokens the model has to emit, so a tool that returns a large payload is expensive
even when it answered instantly. Asking "how many models are in the registry" and asking "report
exactly what `list_models` returns" differ by more than an order of magnitude in elapsed time
against the same call. This is why the read tools are summary-first with opt-in `detail='full'`
rather than returning everything and letting the caller filter.

**A clean `validate_model` is not proof that a deck runs.** TRACE applies checks SNAP does not.
Confirm with an actual `run_trace` before reporting success.

**If a client exposes tools under a prefix, use the client's name for them.** Server keys
containing a hyphen are a known trap: some clients derive the tool name from the key, and a model
that emits the hyphen back as an underscore gets `tool not found`, retries, and exits successfully
having printed nothing — with no log line naming the cause. Prefer a key with no hyphen when the
client's naming scheme is unknown.

---

---

## snap-melcor — companion MELCOR2X MCP server

Lives in `snap-melcor/`. Mirrors the snap-trace structure but talks to `snap.codes.melcor` instead of `snap.codes.trace`.

### Architecture

```
snap-melcor/
  mcp_server.py               ← entry point
  snap_melcor/
    snap_env.py               ← SNAP path bootstrap + melcor import (stdout fix)
    session.py                ← model registry (in-memory only, no SQLite)
    bindings/
      components.py           ← auto-generated wrappers (278 classes)
      enums.py                ← auto-generated enum classes (203 enums)
    tools/
      model_tools.py          ← melcor_status, create_model, import_melgen,
                                 open_med_model, list_models, close_model
      component_tools.py      ← add_component, list_components, get_component,
                                 get_component_schema, set_component_property,
                                 list_component_properties
      export_tools.py         ← validate_model, export_melgen, save_med
```

### Key API facts (MELCOR2X 2.7.1 on RHEL9)

**No blank-canvas model creation.** `snap.codes.melcor` has no `create_model()`. `create_model` writes a minimal MELGEN title card to a temp file, calls `mc.import_melgen(tmp)`, and deletes the temp file.

**Component creation pattern:**
```python
cats = list(jm.getCategories())
cat = next(c for c in cats if "CVH" in str(c.getShortName()).upper())
comp = cat.createComponent(jm)
comp.addToModel(jm)
comp.setName("CV-DOME")
```
Category short names are full display strings like `"Control Volumes (CVH)"` — match by substring, not exact equality.

**Java class names** (confirmed via `obj.getClass().getSimpleName()`):
- CVH → `VolumeComponent`
- FL → `FlowPath`
- HS → `HeatComponent`
- NCG → `NCGasComponent`

`type(obj).__name__` always returns `"JavaObject"` in Py4J — always use `getClass().getSimpleName()` for type identification.

**Property setter dispatch (CReal pattern):**
MELCOR unit-typed setters (`setPvolr`, `setTatmr`, etc.) take SNAP `CReal` subclass objects (Pressa, Temp, Length…), not raw Python floats. Py4J cannot auto-coerce across classloaders. Pattern:
```python
creal_obj = java_comp.getPvolr()   # get existing CReal instance
creal_obj.setValue(float(value))   # mutate in-place
java_comp.setPvolr(creal_obj)      # pass back
```
`LengthControlArc` setters (diamf, diamr, zfm, zto) need an extra indirection:
```python
arc = java_comp.getDiamf()
arc.getLength().setValue(float(value))
arc.setLength(arc.getLength())
```
CV reference setters (`setKcvfm`, `setKcvto`) take an integer CC number. If a string name is passed, resolve it to CC# via `_find_component(jm, name).getCCnumber()`.

All four dispatch paths are implemented in `_call_setter()` in `component_tools.py`.

**`open_med_model` bug:** `snap.codes.melcor.open_model()` checks `plugin_id != "MELCOR"` but the actual plugin ID is `"MELCOR2X"` → always raises `ValueError`. Use `snap.model_editor.open_model(path)` directly.

**`sys.stdout` hijack:** `snap.codes.melcor` replaces `sys.stdout` with a `_StreamLogHandler` on import (same as `snap.codes.trace`). Fixed in `snap_env.py` by saving/restoring real stdout around the import.

**Human-friendly property aliases** (`_PROPERTY_ALIASES` in `component_tools.py`):
- CVH: `volume→pvolr`, `pressure→pncg`, `temperature→tatmr`, `pool_temp→tpolr`, `pool_elevation→zpolr`
- FL: `from_cv→kcvfm`, `to_cv→kcvto`, `flow_area→flara`, `diameter→diamf`, `length→fllen`, `elevation_from→zfm`, `elevation_to→zto`
- HS: `geometry→igeom`, `initial_temp→initialTemp`, `left_bc→ibcl`, `right_bc→ibcr`, `left_htc→xhtfcl`, `right_htc→xhtfcr`

**Default model components:** Every new MELCOR model auto-creates three NCG components — POOL (cc=1), FOG (cc=2), H2O-VAP (cc=3). These are MELCOR defaults and cannot be removed.

**`validate_model` fallback:** MELCOR's `java_model.validate()` may not exist; the tool falls back to a temp-file export check.

---

## Dependencies

| Package | Role |
|---------|------|
| `mcp[cli]>=1.0` | FastMCP framework; tested against v1.27.1 |
| `pydantic>=2.0` | Used internally by FastMCP |
| `snap.codes.trace` | SNAP Python API (bundled with SNAP installation, not on PyPI) |
| `snap.codes.melcor` | SNAP MELCOR2X Python API (requires melcor2x.jar in SNAP plugins/) |
| `py4j` | JVM bridge used by the SNAP API |
| `anyio` | Async I/O; pulled in by `mcp` |
