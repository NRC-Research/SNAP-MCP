"""MCP resources: static reference material for the AI agent."""
from __future__ import annotations

from pathlib import Path

from snap_trace.component_map import ALL_TYPES, COMPONENT_MAP

_SNAP_SAMPLES = Path.home() / "run-snap500" / "Samples" / "TRACE"
_GUIDELINES = Path(__file__).parent.parent / "SNAP-TRACE-plugin" / "docs"


def register(mcp):

    @mcp.resource("trace://component-types")
    def component_types() -> str:
        """All supported TRACE component types and their roles."""
        lines = ["# TRACE Component Types\n"]
        lines.append(
            "Use get_component_schema(type) for detailed property information.\n"
        )
        categories = {
            "Hydraulic (fluid flow)": [
                "PIPE", "FILL", "BREAK", "PUMP", "VALVE",
                "VESSEL", "PLENUM", "TEE", "SEPARATOR", "TURBINE",
            ],
            "Heat Transfer": ["HEAT_STRUCTURE", "HEATER"],
            "Control & Instrumentation": [
                "CONTROL_BLOCK", "SIGNAL_VARIABLE", "SIGNAL_EXPRESSION",
                "TRIP", "TRIP_CONTROLLER",
            ],
            "Power": ["POWER"],
            "Containment": [
                "CONTAN_COMPARTMENT", "CONTAN_HEAT_STRUCTURE",
                "CONTAN_COOLER", "CONTAN_FAN_COOLER",
                "CONTAN_PASSIVE_JUNCTION", "CONTAN_FORCED_JUNCTION",
                "CONTAN_SINK_JUNCTION",
            ],
        }
        for cat, types in categories.items():
            lines.append(f"\n## {cat}\n")
            for t in types:
                lines.append(f"- **{t}**: create_method=`{COMPONENT_MAP[t]['create']}`")
        return "\n".join(lines)

    @mcp.resource("trace://connection-syntax")
    def connection_syntax() -> str:
        """How to connect TRACE components via hydraulic junctions."""
        return """\
# TRACE Connection Syntax

## Pattern (from standpipe.py example)

    break_11.inlet = ("[JUN2] Outlet", 21, 20)
    pipe_21.inlet  = ("[JUN1] Inlet",   1,  1)

## MCP Tool: connect_components

    connect_components(
        model_id         = "...",
        component_number = 11,          # the component whose face is being set
        face             = "inlet",     # which face: "inlet" | "outlet" | "side"
        target_junction_slot = "[JUN2] Outlet",  # face label on the TARGET
        target_component_number = 21,   # the other component
        target_cell_index = 20,         # cell on the target (1 = first, N = last)
    )

## Standard Junction Slot Labels

| Slot string      | Meaning                        |
|------------------|--------------------------------|
| "[JUN1] Inlet"   | First junction (inlet face)    |
| "[JUN2] Outlet"  | Second junction (outlet face)  |
| "[JUN3] Side"    | Side/crossflow junction (TEE)  |

## Example: Simple Loop (Fill → Pipe → Break)

    # Fill 1 outlet → Pipe 21 inlet (cell 1)
    connect_components(model_id, 21, "inlet", "[JUN1] Inlet", 1, 1)

    # Pipe 21 outlet (cell 20) → Break 11 inlet
    connect_components(model_id, 11, "inlet", "[JUN2] Outlet", 21, 20)

## Notes
- Junction numbers are managed internally by SNAP.
- Each face may only be connected once.
- For VESSEL components, use the vessel's face/level-specific connection API.
"""

    @mcp.resource("trace://example/standpipe")
    def standpipe_example() -> str:
        """The complete Standpipe example script from SNAP Samples."""
        p = _SNAP_SAMPLES / "Standpipe" / "standpipe.py"
        if p.exists():
            return p.read_text()
        return "(standpipe.py not found — expected at ~/run-snap500/Samples/TRACE/Standpipe/standpipe.py)"

    @mcp.resource("trace://enum-reference")
    def enum_reference() -> str:
        """Common TRACE enum classes and selected values."""
        return """\
# Common TRACE Enum Values

Pass these as strings to add_component/set_component_property.
Format: "ClassName.MethodName"  (no parentheses needed in JSON/tool calls)

## BreakIbtySel (Break boundary type)
- BreakIbtySel.No_Tables
- BreakIbtySel.Input_Pressure_Table

## BreakIsatSel (Break saturation state)
- BreakIsatSel.Set_liquid_and_gas_to_Tsat

## BreakIoffSel (Break pressure option)
- BreakIoffSel.Input_Pressure_Maintain_State

## FillIftySel (Fill type)
- FillIftySel.Gen_State_CS
- FillIftySel.Liquid_Only
- FillIftySel.Mass_Flow_Rate

## ControlTypeSel (Control block type — required for CONTROL_BLOCK)
- ControlTypeSel.Interactive_Variable
- ControlTypeSel.PID
- ControlTypeSel.Table_1D
- ControlTypeSel.Constant

## SignalTypeSel (Signal variable type — required for SIGNAL_VARIABLE)
- SignalTypeSel.Liquid_Temperature
- SignalTypeSel.Vapor_Temperature
- SignalTypeSel.Pressure
- SignalTypeSel.Void_Fraction
- SignalTypeSel.Fluid_Velocity_Across_Z_Axis
- SignalTypeSel.Slab_Rod_Surface_Temp
- SignalTypeSel.Mass_Flow_Rate

## SignalVariableMode
- SignalVariableMode.EXACT
- SignalVariableMode.AVERAGE

## HeatStructureGeometry
- HeatStructureGeometry.CYLINDRICAL
- HeatStructureGeometry.SLAB
- HeatStructureGeometry.ANNULAR

## NffSel (Junction friction flag)
- NffSel.FlowFactorAndFric

## CalculationFlag (Pipe geometry specification)
- CalculationFlag.Area
- CalculationFlag.Volume

## NLSiEngSel (Unit system)
- NLSiEngSel.SI_Units
- NLSiEngSel.English_Units

## NLNoairSel (Non-condensable gas)
- NLNoairSel.NC_Calc_On
- NLNoairSel.NC_Calc_Off
"""

    @mcp.resource("trace://reference/materials")
    def materials_reference() -> str:
        """Standard TRACE material numbers, roughness values, and heat structure guidance."""
        return """\
# TRACE Material Reference

Source: NRC TRACE PWR Modeling Guidance Rev 1.

## Standard Material Numbers (MATRD)

| Material # | Material | Typical Use |
|-----------|----------|------------|
| Material 1 | UO₂ fuel | Fuel pellet zones in fuel rod HTSTR |
| Material 2 | Zircaloy | Fuel rod cladding, core thimble tubes |
| Material 8 | Stainless steel | General structural components |
| Material 9 | Carbon steel | RPV barrel, baffle, shell; SG barrel/shroud |
| Material 12 | Inconel 600 | SG U-tubes, OTSG tubes |

## Wall Surface Roughness (EPSW)

| Surface | EPSW (m) | Notes |
|---------|----------|-------|
| Commercial steel pipe | 4.572e-5 | Primary loops, cold/hot legs, most piping |
| Drawn tubing (SG) | 1.524e-6 | SG U-tubes, OTSG tubes |
| Smooth (default) | 0.0 | Only for explicitly smooth surfaces |

## Radial Node Guidance for HEAT_STRUCTURE

| Structure | Nodes | Layout |
|-----------|-------|--------|
| Fuel rods | **8** | 5 UO₂ pellet + 1 gap + 2 Zircaloy cladding |
| SG tubes (Inconel) | **4** | Adequate for thin-walled tube |
| RPV/SG barrel, baffle | wall_in / 0.1 + 1 | ~0.1 inch per node |
| Thick structures | log₂(1 + thickness_m/0.0254) + 1 | Logarithmic spacing |

## Geometry Type (HSCYL)

| Type | When to use |
|------|-------------|
| CYLINDRICAL (HSCYL=1) | Fuel rods, SG tubes, RPV/SG barrel/shell, thimble tubes |
| SLAB (HSCYL=0) | RPV baffle, CRGTs, secondary separators, RCPs, SG plena |

## Initial Temperature (RFTN)

| Structure | Initial Temperature |
|-----------|-------------------|
| SG tubes, barrel, separators | SG secondary-side T_sat |
| RPV barrel, baffle, shell, thimble tubes, CRGTs | RV average moderator temperature |
| Fuel rods | Average core coolant temperature |
| Other structures | Temperature of surrounding fluid |

## Fine Mesh Nodalization (NFAX / DZNHT)

Recommended settings for fuel rod heat transfer (NRC sensitivity study, Bajorek):

| Parameter | Value | Notes |
|-----------|-------|-------|
| NFAX | 3 | Permanent heat transfer nodes per axial cell |
| DZNHT | 0.001 m | Minimum fine mesh node size |
| FM renodalization | On | Converged results for reflood at low CPU cost |

Increasing NFAX to 5 reduces PCT by ~15 K at modest cost. Very fine fixed meshes (NFAX=331)
cost ~45× more CPU with only ~5 K additional improvement.
"""

    @mcp.resource("trace://reference/friction")
    def friction_reference() -> str:
        """Friction factor (NFF) and loss coefficient (KFAC) guidance for PIPE components."""
        return """\
# TRACE Friction and Loss Coefficient Reference

Source: NRC TRACE PWR Modeling Guidance Rev 1, §1 General Guidance.

## NFF — Junction Friction Flag

| NFF | Meaning | When to use |
|-----|---------|-------------|
| 1 | TRACE computes wall friction via Churchill correlation | Default — use for all straight pipe runs |
| 0 | Friction disabled; analyst provides KFAC | Required at edges with significant flow area changes |

**Critical constraint when NFF=0:** Both cells adjacent to that edge must satisfy:
    DX ≥ 0.625 × HD
This ensures unmodeled wall friction is negligible compared to the specified form loss.

## KFAC — Forward Loss Coefficient (and KFACR — Reverse)

| Geometry | KFAC (forward) | KFACR (reverse) | Reference |
|----------|----------------|-----------------|-----------|
| Sudden contraction | 0.5 × (1 − β²) | (1 − β²)² | Crane p. 2-11 |
| Sudden expansion | (1 − β²)² | 0.5 × (1 − β²) | Crane p. 2-11 |
| 90° standard elbow | 30 × f_T | 30 × f_T | Crane p. A-29 |
| 45° standard elbow | 16 × f_T | 16 × f_T | Crane p. A-29 |
| Close-pattern return bend | 50 × f_T | 50 × f_T | Crane p. A-29 |
| Standard tee (branch flow) | 60 × f_T | 60 × f_T | Crane p. A-29 |

where β = D_small / D_large and f_T is the Darcy friction factor for fully turbulent flow
in smooth commercial steel pipe (typically 0.013–0.020 depending on diameter).

## 10:1 Volume Ratio Rule

The volume ratio of any cell to any directly adjacent cell must not exceed **10:1**.
Subdivide cells or adjust DX arrays if this is violated.
Exception: 1-D to 3-D connections (e.g. CRGT to RPV VESSEL cells).

## Example — Cold Leg with Area Change at Pump Nozzle

Edge at pump suction nozzle (contraction from cold leg to pump inlet):
    β = D_pump_inlet / D_cold_leg ≈ 0.75
    KFAC  = 0.5 × (1 − 0.75²) = 0.22   (contraction, forward flow into pump)
    KFACR = (1 − 0.75²)²       = 0.19   (expansion, reverse flow out of pump)
    NFF   = 0 (area change edge)
    DX adjacent cells ≥ 0.625 × HD

## Valve Flow Capacity Verification

After modeling PORV, SRV, MSSV, or other valves:
1. Set valve fully open (FAVLVE = 1.0)
2. Set upstream pressure to rated pressure
3. Run short transient
4. Compare calculated flow to rated capacity
5. Adjust KOPEN or AVLVE as needed
"""

    @mcp.resource("trace://reference/component-numbering")
    def component_numbering() -> str:
        """NRC standard PWR component numbering scheme."""
        return """\
# NRC Standard PWR Component Numbering Scheme

Source: NRC TRACE PWR Modeling Guidance Rev 1, Appendix A.24.

Not required for a valid model but recommended for consistency across NRC PWR models,
re-use of plotting scripts, and minimal conflicts when copying control systems.

## General Rules

- All thermal-hydraulic components: **1000–1999** (reserves 3-digit space for PARCS coupling)
- Fuel HTSTR components: **100–999** (3-digit, PARCS-compatible)
- Numbers increment by **5** (leaves room for extra components)
- Numbers increment in the direction of typical liquid flow
- Pipe wall HTSTRs: component_number × 1000 + 1

## Primary System (1000–1499)

| Number | Component |
|--------|-----------|
| 1000 | RPV VESSEL |
| 1010 | Pressurizer |
| 1015 | Pressurizer surge line |
| 1020 | PORV VALVE |
| 1025 | PORV BREAK |
| 1030 | SRV VALVE |
| 1035 | SRV BREAK |
| 1040 | Pressurizer spray suction line |
| 1090 | Split break BREAK |
| 1091 | Split break SJC |
| 1092, 1093 | DEG break BREAKs |

### Per-Loop Primary (Loop N → 1N00 series)

| Offset | Component |
|--------|-----------|
| +00 | Hot leg |
| +05 | SG inlet plenum |
| +10 | SG tubes (UTSG) or OTSG tubes |
| +15 | SG outlet plenum |
| +20 | Intermediate leg A |
| +25 | Pump suction A |
| +30 | Pump A |
| +35 | Cold leg A |
| +40 | Accumulator tank A |
| +45 | Accumulator line A |
| +50 | Intermediate leg B (2 cold legs/loop) |
| +55–+65 | Pump B, cold leg B, accumulator B |
| +80–+85 | HPSI/LPSI, charging, letdown |

Example: Loop 1 hot leg = 1100; Loop 2 pump A = 1230; Loop 3 cold leg B = 1365

## Secondary System (1500–1899)

Per-loop secondary uses (Loop+4)×100 series:

| Offset | Component |
|--------|-----------|
| +00 | SG downcomer |
| +10 | SG boiler region |
| +15 | SG separator (UTSG) |
| +20 | SG steam dome |
| +25 | MSL/MSIV |
| +30–+35 | MSSV VALVE and BREAK |
| +40–+45 | ADV VALVE and BREAK |
| +50–+70 | Turbine stop/control valves, bypass |
| +75 | Main FW line |
| +80 | Main FW FILL |
| +81 | AFW FILL |

Example: Loop 1 SG downcomer = 1500; Loop 2 MSL = 1625; Loop 3 FW FILL = 1780

## RPV Internal Components (1900–1999)

| Range | Component |
|-------|-----------|
| 1900–1915 | Core thimble tubes (up to 8 sectors × 2 rings) |
| 1920–1935 | Control rod guide tubes |
| 1940–1947 | Reactor vessel vent valves |
| 1970 | Pressurizer boundary isolation valve (SS init only) |
| 1971 | Steady-state pressure BREAK (SS init only) |
| 1999 | Reactor POWER component |

## Fuel HTSTR Components (100–999)

Pattern: Ring × 100 + Sector × 10 + Burnup_group

| Example | Meaning |
|---------|---------|
| 110 | Ring 1, Sector 1, fresh fuel |
| 232 | Ring 2, Sector 3, twice-burned |

## Steady-State Initialization Components

During SS initialization, add a temporary pressure boundary:
- VALVE 1970 (isolation valve, open during SS, closed for transient)
- BREAK 1971 (constant pressure = target pressurizer pressure, IBTY=0, ALPIN=1.0)
"""

    @mcp.resource("trace://workflow/analyst-guidance")
    def analyst_guidance() -> str:
        """Scope, best practices, and limitations for analysts using snap-trace."""
        return """\
# snap-trace MCP — Analyst Guidance

## What this tool is good for

- **Prototyping a nodalization** — build a FILL → PIPE → BREAK skeleton quickly
- **Translating an existing TRCIN** — import ASCII, inspect, regenerate with corrections
- **Component-level test cases** — isolated subsystem models (SG leg, accumulator, break segment)
- **Parameter studies** — scripted generation of many similar models
- **Learning TRACE model structure** — ask what properties each component type needs

## What it is NOT suited for

- **Full plant models in one pass** — a complete 4-loop PWR has hundreds of components.
  Build subsystems first, assemble the rest in SNAP GUI.
- **Final QA-ready production models without review** — always validate the exported TRCIN
  against NRC modeling guidance before using results analytically.
- **VESSEL (3-D) detailed initialization** — VESSEL creation is supported but per-cell
  ring initialization is not yet implemented.
- **PARCS kinetics coupling** — not implemented.
- **Replacing the SNAP GUI** — the GUI has visualization and drag-and-drop connections.
  Use it for complex topologies; use this MCP for scripted/AI-assisted construction.

## Modeling guidance reference

**Always consult the NRC TRACE Modeling Guidelines before building any component:**

    https://nrc-research.github.io/TRACE_guidance/

Key sections:
- General Guidance — NFF, KFAC, EPSW, 10:1 volume ratio rule
- Heat Structures — radial nodes, material numbers, geometry type, RFTN initialization
- Initialization — steady-state procedure, pressure boundary conditions
- Break Modeling — DEG vs split, cell sizing near break (L/D 0.25–3.0)
- Component Numbering — NRC standard scheme (1000–1999 T-H, 100–999 fuel HTSTR)

MCP resources with extracted summaries of these sections:
- trace://reference/materials      — material numbers, roughness, HS node counts, fine mesh
- trace://reference/friction       — NFF/KFAC formulas, 10:1 rule, valve verification
- trace://reference/component-numbering — NRC standard PWR numbering scheme

## Parameter defaults from guidance (always set these explicitly)

| Component | Parameter | Guidance default | Reason |
|-----------|-----------|-----------------|--------|
| BREAK / FILL | dxin | 1e-6 m | No physical length — negligible |
| BREAK / FILL | volin | 1e6 m³ | Large reservoir — pressure stays fixed |
| BREAK | rbmx | 1e20 | Unconstrained pressure ratio |
| BREAK | isat | 3 (always) | Always set to T_sat |
| BREAK | alpin | 0.0 normal / 1.0 LOCA | 1.0 = steam/gas space at break |
| PIPE | epsw | 4.572e-5 m steel, 1.524e-6 m SG tubing | Wall roughness affects friction |

## Known SNAP API limitations (do not attempt these)

- FILL.name — no setter; omit 'name' from FILL properties
- fluid_segment — setter is broken for plain strings; never set via MCP
- nfax — per-cell array; use set_component_property with a list after creation
- hcom coupling — three levels deep; always use connect_heat_structure, not set_component_property

## Suggested workflow

1. snap_status()                         — confirm SNAP is ready
2. get_component_schema(type)            — read guidance before each new component type
3. create_model(name)                    — start a new model
4. add_component(FILL, BREAK)            — boundary conditions first
5. add_component(PIPE/PUMP/VALVE/TEE)    — hydraulic components
6. connect_components()                  — wire hydraulic junctions
7. add_component(HEAT_STRUCTURE)         — if needed
8. connect_heat_structure()              — wire HS surfaces to hydraulic cells
9. validate_model()                      — MUST pass before saving; fix all errors first
10. save_med(output_path)                — PRIMARY save artifact; version-independent binary
    # Open this .med file directly in SNAP model editor for review.
    # DO NOT use export_trcin for model review — .inp files are TRACE-version
    # sensitive and will fail to import if the SNAP plugin and installed TRACE
    # binary versions differ.
11. export_trcin(output_path)            — ONLY when you need a runnable TRACE deck;
    # requires SNAP_TRACE_TARGET_VERSION to match the installed TRACE binary.

## Why .med, not .inp, for model handoff

SNAP's export always writes the TRCIN format for the TRACE version the plugin
was built against.  If the installed TRACE binary is a different patch level,
the .inp will fail to import with card-format errors.  The .med binary format
is SNAP-internal and is not sensitive to TRACE version.  Always save_med after
validate_model; only export_trcin when preparing to run a TRACE calculation.
"""

    @mcp.resource("trace://workflow/new-model")
    def workflow_new_model() -> str:
        """Step-by-step workflow for building a TRACE model from scratch."""
        return """\
# Workflow: Build a TRACE Model from Scratch

## 1. Check SNAP status
    snap_status()   # wait until ready=true

## 2. Create model
    create_model(name="My Loop", version="V5.0p9")
    # → returns { model_id: "abc12345" }

## 3. (Optional) Set model options
    # Model options are accessible via model.model_options() in raw Python.
    # For now, defaults are reasonable for most models.

## 4. Add boundary conditions first (Fill, Break)
    add_component(model_id, "FILL", 1, {
        "ifty": "FillIftySel.Gen_State_CS",
        "dxin": 2.0, "volin": 0.146,
        "alpin": 0.0, "tlin": 420.0, "tvin": 420.0,
        "pin": 6e5, "pain": 0.0, "flowin": 5.0
    })

    add_component(model_id, "BREAK", 11, {
        "ibty": "BreakIbtySel.No_Tables",
        "isat": "BreakIsatSel.Set_liquid_and_gas_to_Tsat",
        "ioff": "BreakIoffSel.Input_Pressure_Maintain_State",
        "dxin": 1e-6, "volin": 1e6,       # guidance defaults
        "alpin": 0.0, "tin": 420.0, "pin": 4e6, "pain": 0.0,
        "rbmx": 1e20
    })

## 5. Add hydraulic components (Pipe, Pump, Valve, etc.)
    add_component(model_id, "PIPE", 21, {}, initializer={
        "nsegs": 20, "n_pipes": 1, "length": 4.0,
        "hd": 0.3048, "horizontal": False
    })

    # Then set initial conditions (one row per cell):
    set_component_property(model_id, "PIPE", 21,
        "fluid_segment.initial_conditions_cell_table",
        [[6e5, 432.0, 432.0, 0.0, 0.0]] * 20)

## 6. Connect components
    connect_components(model_id, 21, "inlet", "[JUN1] Inlet", 1, 1)
    connect_components(model_id, 11, "inlet", "[JUN2] Outlet", 21, 20)

## 7. Add heat structures (if needed)
    add_component(model_id, "HEAT_STRUCTURE", 31, {}, initializer={
        "axial": 20, "radial": 9, "length": 4.0,
        "inner": 0.25, "hsycl": "HeatStructureGeometry.CYLINDRICAL",
        "th": 9.27e-3, "temp": 420.0, "material": "Material 8"
    })

## 8. Validate — fix all errors before saving
    validate_model(model_id)

## 9. Save .med  ← PRIMARY ARTIFACT
    save_med(model_id, "/path/to/output.med")
    # Open this file in SNAP model editor for review.
    # .med is SNAP's native binary format — no TRACE version sensitivity.
    # NEVER ask the user to import a .inp file for review purposes.

## 10. Export TRCIN  ← only if running TRACE
    result = export_trcin(model_id, "/path/to/output.inp")
    # Returns {path, bytes, lines} — NOT the deck contents. A plant model is
    # well over a megabyte; returning it inline exhausts the context window.
    # To inspect the deck, search it instead of dumping it:
    #     export_trcin(model_id, pattern="grav")     → matching lines + numbers
    #     export_trcin(model_id, pattern="^sepd")    → the separator cards
    # Only needed to actually run a TRACE calculation.
    # .inp format is tied to the TRACE version the SNAP plugin targets;
    # set SNAP_TRACE_TARGET_VERSION to match the installed TRACE binary.
"""
