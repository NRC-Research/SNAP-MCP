# snap-melcor MCP server

MCP server for MELCOR2X input deck manipulation via SNAP's Python API.
Exposes tools over MCP stdio so an AI analyst can open, inspect, modify,
and export MELCOR models without leaving a Crush session.

**Status: bindings generated and tools implemented — needs live testing.**
The Python bindings were auto-generated from the SNAP-MELCOR-plugin Java source.
All MCP tool stubs have been replaced with real implementations. The next step
is verifying the Java category API works correctly against an actual SNAP
MELCOR2X installation (see [What needs live testing](#what-needs-live-testing)).

---

## What it does

- Open an existing MELGEN `.med` file or import a MELGEN ASCII `.inp`
- Inspect control volumes (CVH), flow paths (FL), heat structures (HS),
  core components (COR), and other packages
- Read and modify component properties via auto-generated Python bindings
- Validate the model and export back to MELGEN input

## What it does NOT do (at least initially)

- Build a MELCOR model from scratch via natural language — MELCOR's package
  structure (CVH/FL/HS/COR/RN) is too interdependent for reliable generation
  without substantial domain scaffolding
- Full core (COR) modeling — the COR package has complex debris/melt
  state that doesn't map cleanly to individual property edits
- RELAP5/TRACE parity — MELCOR's Python API is thinner than TRACE's

---

## MELCOR vs. TRACE — what's different for the MCP

| TRACE (snap_trace) | MELCOR (snap_melcor) |
|---|---|
| Rich Python API: `get_property`, `set_property`, `connect` | Thin Python API: `import_melgen`, `open_model`, `export` only |
| Components are discrete objects (PIPE, FILL, BREAK, HTSTR) | Organized by packages: CVH, FL, HS, COR, RN, BUR, … |
| Build from scratch is practical | Modify existing models is the primary workflow |
| 1 component = 1 SNAP object | 1 CVH control volume ≈ many sub-records (IC, BP, etc.) |
| TRACE plugin ~500 component classes | MELCOR plugin ~278 Java component BeanInfo classes |

### MELCOR package map

| Package | What it models | TRACE analogue |
|---|---|---|
| CVH | Control volumes (containment cells, RCS nodes) | PIPE / PLENUM / VESSEL |
| FL | Flow paths between CVs | Junctions |
| HS | Heat structures (walls, fuel rods) | HTSTR |
| COR | Reactor core (fuel, cladding, debris) | VESSEL internals |
| BUR | Hydrogen combustion | — |
| DCH | Direct containment heating | — |
| RN | Radionuclide / fission product transport | — |
| ESF | Engineered safety features (ECCS, etc.) | — |
| SP | Spray systems | — |
| CF | Control functions | SIGNAL / TRIPS |

---

## Tool set

### Status / session
| Tool | Status | Description |
|---|---|---|
| `melcor_status` | ✅ implemented | Check MELCOR2X plugin is loaded; return version |
| `list_models` | ✅ implemented | List open MelgenModel sessions |
| `close_model` | ✅ implemented | Close a model session and release resources |

### Model I/O
| Tool | Status | Description |
|---|---|---|
| `import_melgen` | ✅ implemented | Import ASCII MELGEN `.inp`; returns model_id |
| `open_med_model` | ✅ implemented | Open `.med` file; returns model_id |
| `export_melgen` | ✅ implemented | Export to MELGEN ASCII input |
| `save_med` | ✅ implemented | Save current state as `.med` |

### Inspection
| Tool | Status | Description |
|---|---|---|
| `list_components` | ✅ implemented | List components, optionally filtered by package (CVH/FL/HS/…) |
| `get_component` | ✅ implemented | Get all properties of a named component |
| `get_component_schema` | ✅ implemented | Describe the properties available for a component type |

### Modification
| Tool | Status | Description |
|---|---|---|
| `set_component_property` | ✅ implemented | Set a property on a component |

### Validation
| Tool | Status | Description |
|---|---|---|
| `validate_model` | ✅ implemented | Run SNAP's built-in model validation; return errors/warnings |

---

## Python bindings

SNAP's MELCOR2X plugin only exposes thin Python bindings (`import_melgen`,
`open_model`, `export`). Component-level property access requires wrapping
the Py4J Java objects. The TRACE plugin ships a 46 K-line `components.py`
generated the same way; we replicated that for MELCOR.

The bindings are auto-generated from the SNAP-MELCOR-plugin Java source:

```
snap_melcor/bindings/
  enums.py       — 203 enum classes (from editors/enums/*SelEditor.java)
  components.py  — 278 component wrapper classes (from components/*BeanInfo.java)
```

To regenerate after a plugin source update:

```bash
python3 snap-melcor/tools/generate_bindings.py \
    --melcor-src /path/to/SNAP-MELCOR-plugin/src/cfnplugin/melcor \
    --out-dir snap-melcor/snap_melcor/bindings
```

### Key design notes

- `FlowPath` inherits from `AbstractFlowPath` (138 properties); `ControlVolume`
  has 76 properties. Class hierarchy is preserved via topological sort.
- Each class has a `_SCHEMA` dict with `{prop_name: {display, type, description}}`.
  Since properties live on parent classes, always use the MRO-merged version:
  ```python
  def _full_schema(cls):
      s = {}
      for c in reversed(cls.__mro__):
          s.update(getattr(c, '_SCHEMA', {}))
      return s
  ```
- Property types: `real`, `int`, `string`, `bool`, `enum`, `reference`,
  `real_optional`, `tabfunc_ref`, `ctlfunc_ref`
- The bindings can be imported without SNAP installed (stub base classes are
  used); `_SCHEMA` introspection works offline.

---

## What needs live testing

The tools are implemented but the following have never been run against an
actual SNAP MELCOR2X installation. Each item is a potential failure point.

### 1. Category short names for `findCategoryByShortName()`

Component access uses `java_model.findCategoryByShortName(pkg)` with strings
like `"FL"`, `"CVH"`, `"HS"`. **Verify** these match what the MELCOR2X plugin
registers as category short names. If they differ, update the `packages_to_query`
list in `component_tools.py`.

```python
# Probe on a live model:
from snap.codes.melcor import open_model
m = open_model("test.med")
for cat in m.java_model.getCategories():
    print(cat.getShortName(), cat.getName())
```

### 2. `getComponents()` method name

`list_components` calls `java_category.getComponents()`. Verify this method
exists. Alternatives if it doesn't:
- `java_category.getComponentList()`
- `java_category.components()`
- Iterate via `java_model.getComponents(java_category)`

### 3. `findComponentByName()` method name

`get_component` and `set_component_property` call
`java_model.findComponentByName(name, java_cat)`. Verify the signature.
TRACE uses `findComponentByCC(cc_number, category)` for number-based lookup.
MELCOR may use a name-based equivalent or require iterating `getComponents()`.

### 4. Real property setter pattern

The generated setter for real properties does:
```python
real = self.java_object.getZfm()
real.convert(float(value))
self.java_object.setZfmConstrained(real.getValue())
```
This mirrors the TRACE pattern. Verify it works for MELCOR. The `convert()`
call handles unit conversion (the `Real` Java object stores the value in
internal units but `convert()` accepts user-facing units).

### 5. Enum setter pattern

Generated enum setters pass `.value` (the integer) to `setXxxConstrained()`.
Verify MELCOR's constrained setters accept a raw integer; TRACE's do.

### 6. `save_med` / `save_as` method

`save_med` tries `model.save(path)`, then `model.save_as(path)`, then
`model.java_model.save(path)`. Verify which one works for `MelgenModel`.

---

## Repository layout

```
snap-melcor/
  mcp_server.py                 — entry point; registers all tools
  pyproject.toml                — package metadata (snap-melcor-mcp)
  tools/
    generate_bindings.py        — binding generator script
  snap_melcor/
    __init__.py
    snap_env.py                 — adds SNAP Python path; verifies melcor import
    session.py                  — model session registry (model_id → MelgenModel)
    bindings/
      __init__.py
      enums.py                  — 203 generated enum classes [DO NOT EDIT]
      components.py             — 278 generated component classes [DO NOT EDIT]
    tools/
      model_tools.py            — melcor_status, import_melgen, open_med_model, …
      component_tools.py        — list_components, get_component, set_component_property, …
      export_tools.py           — validate_model, export_melgen, save_med
```

---

## Deployment (not yet done)

Once live testing passes, add `snap-melcor` to the image provisioning:

1. Add the repo clone + pip install to the MCP install role in both the Linux and Windows
   provisioning trees.

2. Register the MCP in the `crush.json` configuration patch applied to the image:
   ```json
   "snap-melcor": {
     "command": "python3",
     "args": ["/opt/crush/snap-melcor/mcp_server.py"],
     "env": { "SNAP_PYTHON_PATH": "/opt/snap/python" }
   }
   ```

3. Add the tool names to `allowed_tools` in the Crush session config.

---

## Reference

- MELCOR Python API: `SNAP-MELCOR-plugin/lib/python/snap/codes/melcor.py`
- MELCOR Java plugin source: `SNAP-MELCOR-plugin/src/cfnplugin/melcor/`
- SNAP model editor API: `~/snap/python/snap/model_editor.py`
- SNAP base property classes: `~/snap/python/snap/codes/properties.py`
- SNAP-TRACE MCP (reference implementation): `../snap_trace/`
