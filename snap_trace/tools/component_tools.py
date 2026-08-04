"""MCP tools: component add / update / list / schema."""
from __future__ import annotations

import math

import snap_trace.session as session
from snap_trace.component_map import (
    ALL_TYPES,
    COMPONENT_MAP,
    create_component,
    find_component,
    invalidate_cc_index,
    iter_all_components,
)
from snap_trace.type_converter import set_property


# ---------------------------------------------------------------------------
# Vessel table helpers
# ---------------------------------------------------------------------------

_CELL_TABLES = frozenset({"p", "tl", "tv", "alp", "pa", "s", "vol_frac"})


def _apply_sector_angles(vessel, num_sectors: int) -> bool:
    """Correct per-sector azimuthal widths (radians) after VESSEL creation.

    SNAP's VesselInitializer may write sector widths in degrees instead of
    radians (producing ~20626 for a single-sector full-circle vessel).
    This corrects the y_nodalization table to 2π/num_sectors per sector.

    Tries multiple SNAP API paths; returns True if any succeeded.
    When False, the caller should warn — the fix requires a TRCIN round-trip.
    """
    import math
    width_deg = 360.0 / num_sectors

    # Approach 1: get_y_nodalization_cell(i).y_angle — the azimuthal sector
    # angle.  The y_nodalization_table is built from the cell's "y_angle"
    # property (NOT "dy" — Cell has no dy attribute, so the old assignment
    # silently no-opped).  Cell.y_angle's getter returns math.degrees(...),
    # so its setter takes DEGREES; a full circle is 360, not 2*pi.
    try:
        for i in range(num_sectors):
            cell = vessel.get_y_nodalization_cell(i)
            cell.y_angle = width_deg
        # Verify the write actually landed (getter returns degrees).
        check = vessel.get_y_nodalization_cell(0).y_angle
        got = float(getattr(check, "value", check))
        if abs(got - width_deg) < 1.0:
            return True
    except Exception:
        pass

    # Approach 3: scalar attribute that sets total azimuthal extent
    total_rad = math.radians(width_deg) * num_sectors
    for attr in ("yang", "ytot", "dang", "ymax", "azimuthal_extent"):
        try:
            setattr(vessel, attr, total_rad)
            return True
        except Exception:
            pass

    return False


def _apply_ring_radii(vessel, ring_radii: list) -> None:
    """Set per-ring radial widths from a list of cumulative outer radii.

    ring_radii = [r0, r1, ...] outer boundary of each ring, innermost first.
    Ring widths: dr[0] = r0 (inner radius assumed 0), dr[i] = r[i] - r[i-1].
    Writes to get_x_nodalization_cell(i).dx for each ring i.
    """
    radii = [float(r) for r in ring_radii]
    widths = [radii[0]] + [radii[i] - radii[i - 1] for i in range(1, len(radii))]
    for i, w in enumerate(widths):
        try:
            cell = vessel.get_x_nodalization_cell(i)
            cell.dx = w
        except Exception:
            pass


def _get_axis_sel(axis_name: str):
    """Return the AxisSel enum value for 'axial', 'azimuthal', or 'radial'."""
    import snap.codes.trace.enums as _enums
    mapping = {
        "axial": _enums.AxisSel.AXIAL,
        "azimuthal": _enums.AxisSel.AZIMUTHAL,
        "radial": _enums.AxisSel.RADIAL,
    }
    fn = mapping.get(axis_name.lower())
    if fn is None:
        raise ValueError(
            f"Unknown axis '{axis_name}'; must be 'axial', 'azimuthal', or 'radial'"
        )
    return fn()


def _get_vessel_table(vessel, table_name: str):
    """Return the Hydro3DPropertyTable for the given name.

    Cell table names (no axis suffix): p, tl, tv, alp, pa, s, vol_frac
    Edge table names (axis suffix required): hd_axial, hd_azimuthal, hd_radial,
        frac_axial, frac_azimuthal, frac_radial, kfac_axial, kfac_azimuthal,
        kfac_radial, vv_axial, vl_axial
    """
    tn = table_name.lower()
    if tn in _CELL_TABLES:
        attr = f"{tn}_table"
        if not hasattr(vessel, attr):
            raise ValueError(f"VESSEL has no attribute '{attr}'")
        return getattr(vessel, attr)

    for axis in ("_azimuthal", "_axial", "_radial"):
        if tn.endswith(axis):
            base = tn[: -len(axis)]
            attr = f"{base}_table"
            if not hasattr(vessel, attr):
                raise ValueError(f"VESSEL has no edge table '{attr}'")
            return getattr(vessel, attr)(_get_axis_sel(axis[1:]))

    valid = (
        "p, tl, tv, alp, pa, s, vol_frac, "
        "hd_axial, hd_azimuthal, hd_radial, "
        "frac_axial, frac_azimuthal, frac_radial, "
        "kfac_axial, kfac_azimuthal, kfac_radial, vv_axial, vl_axial"
    )
    raise ValueError(f"Unknown vessel table '{table_name}'. Valid names: {valid}")


def _broadcast_vessel_value(value, nz: int, nplanar: int) -> list[list[float]]:
    """Broadcast value to a full nz × nplanar grid.

    float/int → uniform across all cells
    list[float] of length nz → per-level (same across all planar cells per level)
    list[list[float]] shape nz × nplanar → full grid, returned verbatim
    """
    # LLMs sometimes pass numeric values as JSON strings — coerce them early.
    if isinstance(value, str):
        value = float(value)
    if isinstance(value, (int, float)):
        return [[float(value)] * nplanar for _ in range(nz)]
    if isinstance(value, list) and value:
        if isinstance(value[0], str):
            value = [float(v) for v in value]
        if isinstance(value[0], (int, float)):
            if len(value) == nz:
                return [[float(v)] * nplanar for v in value]
            raise ValueError(
                f"Flat list has {len(value)} elements; expected {nz} (one per axial level)"
            )
        if isinstance(value[0], list):
            if len(value) != nz:
                raise ValueError(
                    f"Outer list has {len(value)} rows; expected {nz} (one per axial level)"
                )
            return [[float(v) for v in row] for row in value]
    raise ValueError(
        f"Unsupported value type {type(value).__name__}. "
        "Use a float, list[float] (length=nz), or list[list[float]] (nz × nr*nt)."
    )


def _extract_mesh_info(comp) -> dict:
    """Walk the radial mesh of a HEAT_STRUCTURE and return material/geometry info."""
    try:
        mesh = comp.mesh
        if mesh is None:
            return {}
        regions = mesh.material_regions
        layers = []
        for region in regions:
            layer: dict = {}
            try:
                mat = region.material
                if mat is None:
                    layer["material"] = None
                else:
                    # Try several access patterns — ComponentReference wraps a Material
                    mat_name = None
                    for accessor in ("name", "ctitle", "title"):
                        try:
                            val = getattr(mat, accessor)
                            if val is not None and str(val).strip():
                                mat_name = str(val)
                                break
                        except Exception:
                            pass
                    if mat_name is None:
                        # Fall back to string representation of the reference itself
                        mat_name = str(mat).strip() or None
                    layer["material"] = mat_name
            except Exception:
                pass
            try:
                layer["thickness_m"] = float(region.thickness)
            except Exception:
                try:
                    layer["thickness_m"] = str(region.thickness)
                except Exception:
                    pass
            try:
                layer["meshpoints"] = [float(p) for p in region.meshpoints]
            except Exception:
                try:
                    layer["meshpoints"] = str(region.meshpoints)
                except Exception:
                    pass
            layers.append(layer)
        return {"layers": layers} if layers else {}
    except Exception:
        return {}


def _cc(comp) -> int:
    try:
        return int(comp.java_object.getCCnumber())
    except Exception:
        return -1


def _name(comp) -> str:
    try:
        n = comp.name
        return str(n) if n else ""
    except Exception:
        return ""


def _num_or_unset(v):
    """Coerce a SNAP property/wrapper to a float, bool, 'unset', or str.

    Unset VESSEL cells stringify as 'Unknown'; report those as 'unset' so a
    reviewer can spot ICs that were never initialized.
    """
    if v is None:
        return None
    if isinstance(v, bool):
        return v
    try:
        return float(v)
    except Exception:
        pass
    try:
        return float(v.value)
    except Exception:
        pass
    s = str(v)
    return "unset" if "Unknown" in s else s


def _attr_num(obj, name):
    """getattr + _num_or_unset, swallowing access errors."""
    try:
        return _num_or_unset(getattr(obj, name))
    except Exception:
        return None


def _deg(angle_rad):
    """Convert an edge inclination from radians to degrees.

    Passes through None and the 'unset' sentinel unchanged so an
    uninitialized edge is never reported as a plausible 0.0 degrees.
    """
    if not isinstance(angle_rad, (int, float)) or isinstance(angle_rad, bool):
        return angle_rad
    return math.degrees(angle_rad)


def _grav_from_angle(angle_rad):
    """Derive the TRACE GRAV term from an edge's inclination angle.

    GRAV is not a stored field.  In the plug-in, ``Edge.setGrav(g)`` writes
    ``asin(g)`` into ``edgeAngle`` and ``Edge.getGrav()`` returns
    ``sin(edgeAngle)`` -- so GRAV is a derived view of the angle, and the two
    can never disagree.  The Java getter is not surfaced by SNAP's Python
    binding (there is no ``edge.grav``; verified against the running gateway),
    so we reproduce the same relationship here.

    Returns None/'unset' unchanged rather than coercing, because sin() of a
    sentinel would silently produce a plausible-looking number.
    """
    if not isinstance(angle_rad, (int, float)) or isinstance(angle_rad, bool):
        return angle_rad
    return math.sin(angle_rad)


def _read_vessel_grid(table):
    """Read a Hydro3DPropertyTable into (nz, ncols, grid) of coerced values."""
    nz = int(table.row_count)
    nc = int(table.column_count)
    grid = []
    for r in range(nz):
        try:
            row = table[r]
        except Exception:
            row = None
        vals = []
        for c in range(nc):
            cell = None
            if row is not None:
                try:
                    cell = row[c]
                except Exception:
                    try:
                        cell = list(row)[c]
                    except Exception:
                        cell = None
            vals.append(_num_or_unset(cell))
        grid.append(vals)
    return nz, nc, grid


def _summarize_grid(grid):
    """One-line summary of a value grid: uniform / range / UNSET."""
    flat = [v for row in grid for v in row]
    if not flat:
        return "empty"
    if any(v == "unset" or v is None for v in flat):
        return "UNSET — one or more cells have no value"
    nums = [v for v in flat if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if nums and len(nums) == len(flat) and all(v == nums[0] for v in nums):
        return f"uniform {nums[0]:g}"
    if nums:
        return f"varies {min(nums):g}..{max(nums):g}"
    return "n/a"


def register(mcp):

    @mcp.tool()
    def get_component_schema(component_type: str) -> dict:
        """Return the documentation and key properties for a TRACE component type.

        Use this before calling add_component to understand what properties are
        available, which are required, and what enum values are valid.

        Parameters
        ----------
        component_type : str
            One of: PIPE, FILL, BREAK, PUMP, VALVE, VESSEL, PLENUM, TEE,
            SEPARATOR, TURBINE, HEATER, HEAT_STRUCTURE, POWER, CONTROL_BLOCK,
            SIGNAL_VARIABLE, SIGNAL_EXPRESSION, TRIP, TRIP_CONTROLLER,
            CONTAN_COMPARTMENT, CONTAN_HEAT_STRUCTURE, CONTAN_COOLER,
            CONTAN_FAN_COOLER, CONTAN_PASSIVE_JUNCTION,
            CONTAN_FORCED_JUNCTION, CONTAN_SINK_JUNCTION
        """
        ct = component_type.upper()
        if ct not in COMPONENT_MAP:
            return {
                "error": f"Unknown type '{component_type}'",
                "valid_types": ALL_TYPES,
            }

        # Reference the standpipe.py pattern in the description
        schemas = {
            "PIPE": {
                "description": "1-D hydraulic pipe. Requires cell geometry (nsegs/length/hd or explicit arrays). Main hydraulic workhorse.",
                "initializer_fields": {
                    "nsegs": "int — number of axial segments (cells)",
                    "n_pipes": "int — number of parallel pipes (usually 1)",
                    "length": "float — total pipe length (m)",
                    "hd": "float — hydraulic diameter (m)",
                    "horizontal": "bool — True for horizontal orientation",
                },
                "key_properties": {
                    "name": "str — component label",
                    "epsw": "float — wall surface roughness (m). Guidance defaults: commercial steel=4.572e-5 m, drawn tubing (SG)=1.524e-6 m. Use 0.0 only for smooth walls.",
                    "calculation_flag": "enum — CalculationFlag.Area() or CalculationFlag.Volume()",
                    "initial_conditions": "IMPORTANT: pipe ICs cannot be set via set_component_property(). Use set_pipe_ics(model_id, pipe_cc, p, tl, tv, alp) instead. p in Pa, tl/tv in K, alp=0.0 for single-phase liquid.",
                    "fluid_segment.friction_edge_table": "list[list] — rows of [NffSel.FlowFactorAndFric(), friction_factor]. NFF=1 (FlowFactorAndFric) lets TRACE compute friction via Churchill correlation — recommended for most edges. NFF=0 disables wall friction (use with explicit KFAC loss coefficients at area changes); requires DX ≥ 0.625·HD on both adjacent cells.",
                },
                "connection_slots": {"inlet": "[JUN1] Inlet", "outlet": "[JUN2] Outlet"},
                "guidance": {
                    "epsw": {"commercial_steel": 4.572e-5, "drawn_tubing_sg": 1.524e-6},
                    "nff": "Use NFF=1 (default) for all straight runs. Use NFF=0 only at edges with significant area changes, and add KFAC loss coefficients.",
                    "kfac_common": {
                        "sudden_contraction": "0.5*(1 - (D_small/D_large)^2)",
                        "sudden_expansion": "(1 - (D_small/D_large)^2)^2",
                        "90deg_elbow": "30*f_T",
                        "45deg_elbow": "16*f_T",
                        "tee_branch": "60*f_T",
                    },
                    "volume_ratio": "Adjacent cell volumes must not exceed 10:1. Subdivide if needed.",
                },
            },
            "BREAK": {
                "description": "Pressure/temperature boundary condition (outlet). Sets the downstream thermodynamic state.",
                "initializer_fields": {},
                "key_properties": {
                    "name": "str",
                    "ibty": "enum — BreakIbtySel.No_Tables() | BreakIbtySel.Input_Pressure_Table(). IBTY=7 for CONTAN-coupled containment backpressure.",
                    "isat": "enum — BreakIsatSel.Set_liquid_and_gas_to_Tsat() — always use this (isat=3)",
                    "ioff": "enum — BreakIoffSel.Input_Pressure_Maintain_State()",
                    "dxin": "float — equivalent length (m). Guidance default: 1e-6 m (negligibly small — BREAK has no physical length).",
                    "volin": "float — volume (m³). Guidance default: 1e6 m³ (large reservoir — prevents BREAK pressure from changing due to mass exchange).",
                    "alpin": "float — void fraction (0–1). Use 0.0 for subcooled/two-phase outlet; use 1.0 for LOCA break (steam/gas space).",
                    "tin": "float — temperature (K)",
                    "pin": "float — pressure (Pa)",
                    "pain": "float — non-condensable partial pressure (Pa). Set to containment pressure for LOCA breaks.",
                    "adjpress": "bool — False for most analyses",
                    "rbmx": "float — max pressure ratio. Guidance default: 1e20 (unconstrained).",
                },
                "connection_slots": {"inlet": "[JUN1] Inlet"},
                "guidance": {
                    "dxin_default": 1e-6,
                    "volin_default": 1e6,
                    "rbmx_default": 1e20,
                    "isat_always": 3,
                    "alpin_loca": 1.0,
                    "alpin_normal": 0.0,
                },
            },
            "FILL": {
                "description": "Mass flow / thermodynamic state boundary condition (inlet). Supplies fluid to the loop. NOTE: the 'name' property has no setter in the SNAP API — do not include 'name' in add_component properties.",
                "initializer_fields": {},
                "key_properties": {
                    "ifty": "enum — FillIftySel.Gen_State_CS() | FillIftySel.Liquid_Only()",
                    "dxin": "float — equivalent length (m). Guidance default: 1e-6 m (negligibly small).",
                    "volin": "float — volume (m³). Guidance default: 1e6 m³ (large reservoir).",
                    "alpin": "float — void fraction (0–1). Use 0.0 for subcooled liquid inlet.",
                    "tlin": "float — liquid temperature (K)",
                    "tvin": "float — vapor temperature (K)",
                    "pin": "float — pressure (Pa)",
                    "pain": "float — NC partial pressure (Pa)",
                    "flowin": "float — mass flow rate (kg/s)",
                    "vlin": "float — liquid velocity (m/s)",
                    "vvin": "float — vapor velocity (m/s)",
                    "twtold": "float — wall temperature (K, 0=ignore)",
                    "ifasv": "int — signal variable CC# for void fraction (-n for SV)",
                    "ifmlsv": "int — SV for liquid mass flow",
                    "ifmvsv": "int — SV for vapor mass flow",
                    "ifpasv": "int — SV for NC partial pressure",
                    "ifpsv": "int — SV for pressure",
                    "iftlsv": "int — SV for liquid temperature",
                    "iftvsv": "int — SV for vapor temperature",
                },
                "connection_slots": {"inlet": "[JUN1] Inlet"},
                "guidance": {
                    "dxin_default": 1e-6,
                    "volin_default": 1e6,
                    "name_unsettable": "SNAP API bug — Fill.name has no setter; omit from properties dict.",
                },
            },
            "PUMP": {
                "description": (
                    "Centrifugal pump. Use an initializer to set geometry. "
                    "WARNING: SNAP model check will fail if any of the required parameter "
                    "groups below are left at zero — set ALL of them before validate_model."
                ),
                "initializer_fields": {
                    "nsegs": "int — number of cells (usually 1)",
                    "length": "float — equivalent length (m)",
                    "hd": "float — hydraulic diameter (m)",
                },
                "key_properties": {
                    "name": "str",
                },
                "required_parameters": {
                    "RATED VALUES (all must be non-zero)": {
                        "head":    "float — rated head (m). Typical PWR RCP: ~90 m",
                        "flow":    "float — rated volumetric flow (m³/s). Typical RCP: ~0.5 m³/s",
                        "speed":   "float — rated speed (rpm). Typical RCP: ~1500 rpm",
                        "torque":  "float — rated torque (N·m). Attr may be 'tqrat'.",
                        "density": "float — rated fluid density (kg/m³). Typical PWR: ~750 kg/m³. Attr may be 'rhorat'.",
                    },
                    "MOI": {
                        "inertia": "float — effective moment of inertia (kg·m²). Attr may be 'amoi'. Typical RCP: ~100 kg·m²",
                    },
                    "SPEED VALUES (all must be non-zero)": {
                        "initial_speed":    "float — initial pump speed (rpm). Attr may be 'wspd0'. Match rated speed for steady-state.",
                        "off_speed":        "float — speed at which pump is considered off (rpm). Attr may be 'wspdoff'. Typical: 1.0 rpm.",
                        "max_speed_change": "float — maximum speed change per time step (rpm/s). Attr may be 'dwspmax'. Typical: 600 rpm/s.",
                        "speed_scale":      "float — speed scale factor (dimensionless). Attr may be 'wspdscl'. Use 1.0.",
                    },
                    "FRICTION FACTORS (all must be non-zero)": {
                        "fric0..fric3":        "float — frictional torques 0–3 (N·m). Attrs: 'fric0','fric1','fric2','fric3'. Typical: 0.1–1.0",
                        "torque_break_speed":  "float — speed at which friction torque changes regime (rpm). Attr may be 'wspdbrk'.",
                        "low_speed_0..3":      "float — low-speed friction coefficients 0–3. Attrs: 'wspdl0','wspdl1','wspdl2','wspdl3'.",
                    },
                },
                "connection_slots": {"inlet": "[JUN1] Inlet", "outlet": "[JUN2] Outlet"},
            },
            "VALVE": {
                "description": "Flow control valve.",
                "initializer_fields": {
                    "nsegs": "int",
                    "length": "float",
                    "hd": "float",
                },
                "key_properties": {
                    "name": "str",
                    "open_fraction": "float — 0–1 (0=closed, 1=fully open)",
                },
                "connection_slots": {"inlet": "[JUN1] Inlet", "outlet": "[JUN2] Outlet"},
            },
            "VESSEL": {
                "description": (
                    "3-D multi-dimensional reactor vessel (RPV). Use the initializer to set "
                    "geometry and cell count. IMPORTANT: connect external 1-D pipes using "
                    "connect_pipe_to_vessel() — NOT connect_components(). The SNAP VESSEL "
                    "API rejects 1-D junction labels and the connection silently fails."
                ),
                "initializer_fields": {
                    "geometry": "enum — use EXACTLY 'VesselIgeom.CYLINDRICAL' (RPV) or 'VesselIgeom.CARTESIAN'. Do NOT pass 'CYLINDRICAL' alone — the enum prefix is required.",
                    "height": "float — total vessel height (m)",
                    "outer_radius": "float — outer radius of outermost ring (m) [cylindrical only]",
                    "num_levels": "int — number of axial levels (nasx). Typical RPV: 10–20.",
                    "num_rings": (
                        "int — number of radial rings (nrsx). "
                        "Minimum 2 for RPV: ring 1 = core/plenums (inner), ring 2 = downcomer (outer)."
                    ),
                    "num_sectors": (
                        "int — number of azimuthal sectors (ntsx). Use 1 for full 360° symmetric RPV. "
                        "IMPORTANT: SNAP stores all vessel angles in RADIANS. For a single-sector "
                        "full-circle vessel the azimuthal span is 2π ≈ 6.2832 rad — NOT 360. "
                        "Passing 360 causes 'Y Angle is out of range' errors in model check."
                    ),
                    "include_downcomer": "bool — True to configure a downcomer region (sets has_downcomer, idcu, idcl)",
                    "include_core": "bool — True to configure a core region (sets has_core, icru, icrl)",
                    "ivssbf": "int — boundary flag; 0 = standard internal boundary (default)",
                },
                "key_properties": {
                    "vess_type": (
                        "enum — VessType.RPV() | VessType.RECTANGULAR() | VessType.DRYWELL() "
                        "| VessType.FLAT_PLATE() | VessType.TUBE_BANK(). "
                        "Use VessType.RPV() for a pressurized-water reactor vessel."
                    ),
                    "epsw": "float — wall roughness (m). Use 4.572e-5 m (commercial steel) for RPV.",
                    "has_downcomer": "bool — True if vessel has a downcomer annulus (outer ring)",
                    "has_core": "bool — True if vessel has a reactor core region",
                    "idcu": "int — 1-based axial level of the upper downcomer/lower-plenum interface",
                    "idcl": "int — 1-based axial level of the lower downcomer/lower-plenum interface",
                    "icru": "int — 1-based axial level of the upper core boundary",
                    "icrl": "int — 1-based axial level of the lower core boundary",
                },
                "connection_slots": {
                    "tool": "connect_pipe_to_vessel() — NOT connect_components()",
                    "face_labels_cylindrical": [
                        "'Positive Azimuthal' — standard face for external 1-D pipe nozzles",
                        "'Negative Azimuthal' — second pipe at same (level, ring) if needed",
                        "'Positive Radial'",
                        "'Negative Radial'",
                    ],
                    "face_labels_cartesian": [
                        "'Positive X Axis'", "'Negative X Axis'",
                        "'Positive Y Axis'", "'Negative Y Axis'",
                    ],
                },
                "cell_index_formula": {
                    "description": (
                        "connect_pipe_to_vessel() accepts (level, ring, sector) and computes the "
                        "flat cell index automatically. Formula for reference: "
                        "cell = (level-1)*(nr*nt) + (ring-1)*nt + (sector-1) + 1"
                    ),
                    "example_2ring_10level_1sector": {
                        "inner_core_bottom":  "level=1,  ring=1 → cell=1",
                        "downcomer_bottom":   "level=1,  ring=2 → cell=2",
                        "inner_core_top":     "level=10, ring=1 → cell=19",
                        "downcomer_top":      "level=10, ring=2 → cell=20",
                    },
                },
                "guidance": {
                    "simple_RPV_recipe": {
                        "num_rings": 2,
                        "num_levels": 10,
                        "num_sectors": 1,
                        "geometry": "VesselIgeom.CYLINDRICAL",
                        "ring_1": "core + upper/lower plenums (innermost)",
                        "ring_2": "downcomer (outermost)",
                        "cold_leg_inlet": "connect to ring=2, high axial level, 'Positive Azimuthal'",
                        "hot_leg_outlet": "connect from ring=1, top axial level, 'Positive Azimuthal'",
                    },
                    "per_cell_initialization": (
                        "Use set_vessel_table(model_id, vessel_cc, table_name, value) for ICs "
                        "and edge HDs. Cell table names: 'p' (Pa), 'tl' (K), 'tv' (K), "
                        "'alp' (void fraction, 0.0 for subcooled liquid), 'pa' (NC partial pressure Pa). "
                        "Edge table names (REQUIRED — model check fails if these are zero): "
                        "'hd_axial', 'hd_azimuthal', 'hd_radial' (all in meters). "
                        "Typical RPV: hd_axial ≈ 0.4 m (equivalent diameter of core flow area), "
                        "hd_azimuthal and hd_radial ≈ cell cross-section hydraulic diameter. "
                        "value can be a float (uniform), list[float] of length nz (per-level), "
                        "or list[list[float]] of shape nz × (nr*nt) (per-cell full specification). "
                        "Per-cell geometry (axial heights, ring radii) must still be set in the SNAP GUI."
                    ),
                },
            },
            "HEAT_STRUCTURE": {
                "description": "Fuel rod / wall heat structure. Coupled to hydraulic components via inner/outer boundary conditions.",
                "initializer_fields": {
                    "axial": "int — number of axial nodes",
                    "radial": "int — number of radial mesh points. Guidance: fuel rods=8 (5 fuel+gap+2 clad), SG tubes=4, RPV/SG barrel=wall_thickness_inches/0.1+1",
                    "length": "float — total length (m)",
                    "inner": "float — inner boundary radius fraction (0=solid rod, >0 for annular/tube)",
                    "hsycl": "enum — HeatStructureGeometry.CYLINDRICAL (fuel rods, SG/RPV tubes) | HeatStructureGeometry.SLAB (baffle, CRGTs)",
                    "th": "float — wall thickness (m). For fuel rods: OD_clad/2. For tubes: wall thickness only.",
                    "temp": "float — initial temperature (K). Use surrounding fluid temperature.",
                    "material": "str — material name. Standard SNAP materials: 'Material 1'=UO2 fuel, 'Material 2'=Zircaloy clad/thimble, 'Material 8'=stainless steel, 'Material 9'=carbon steel (RPV/SG barrel), 'Material 12'=Inconel 600 (SG tubes).",
                },
                "key_properties": {
                    "name": "str",
                    "nzmax": "int — max axial zones (fine mesh limit). Guidance default: 100.",
                    "rdx": "float — radial mesh refinement factor. Default: 1.0.",
                    "nfcil": "int — number of fuel cells (fuel rods only)",
                    "nfax": "int — fine mesh nodes per axial hydraulic cell. Guidance: NFAX=3. NOTE: this is a per-cell array in the SNAP API; setting it as a scalar via add_component will fail. Use set_component_property with a list of equal values after creation.",
                    "dznht": "float — minimum fine mesh node size (m). Guidance: 0.001 m (1 mm). Set via set_component_property after creation.",
                },
                "connection_slots": {"via connect_heat_structure": "connect_heat_structure(model_id, hs_cc, hs_axial_cell, 'inner'|'outer', hydro_cc, hydro_cell)"},
                "guidance": {
                    "radial_nodes": {
                        "fuel_rod": "8 (5 UO2 pellet + 1 gap + 2 Zircaloy cladding)",
                        "sg_tube": "4 (adequate for thin-walled Inconel)",
                        "rpv_barrel_sg_barrel": "wall_thickness_inches / 0.1 + 1 (~0.1 inch per node)",
                        "thick_structures": "log2(1 + thickness_m / 0.0254) + 1, rounded",
                    },
                    "materials": {
                        "Material 1": "UO2 fuel pellet",
                        "Material 2": "Zircaloy (cladding, thimble tubes)",
                        "Material 8": "stainless steel",
                        "Material 9": "carbon steel (RPV, SG barrel, baffle)",
                        "Material 12": "Inconel 600 (SG tubes)",
                    },
                    "fine_mesh": {"nfax": 3, "dznht_m": 0.001},
                    "geometry": {
                        "CYLINDRICAL": "fuel rods, SG U-tubes, OTSG tubes, SG/RPV barrel/shell, thimble tubes",
                        "SLAB": "RPV baffle, CRGTs, secondary separators, RCPs, SG plena",
                    },
                    "initial_temp": {
                        "SG_tubes_barrel": "SG secondary-side T_sat",
                        "RPV_structures": "RV average moderator temperature",
                        "fuel_rods": "Average core coolant temperature",
                        "other": "Temperature of surrounding fluid",
                    },
                },
            },
            "CONTROL_BLOCK": {
                "description": "Control system block (PID, table, interactive variable, etc.).",
                "initializer_fields": {},
                "key_properties": {
                    "control_type": "enum (REQUIRED) — ControlTypeSel.Interactive_Variable() | ControlTypeSel.PID()",
                    "name": "str",
                    "description": "str",
                    "cbgain": "float — gain",
                    "cbxmin": "float — minimum output",
                    "cbxmax": "float — maximum output",
                    "cbcon1": "float — initial/constant value 1",
                    "cbcon2": "float — initial/constant value 2",
                    "variable_name": "str — display name for interactive variable",
                },
                "connection_slots": {},
                "note": "Negative CC numbers are conventional for control blocks (e.g. -1, -10).",
            },
            "SIGNAL_VARIABLE": {
                "description": "Monitors a physical quantity (temperature, pressure, flow, etc.) at a specific component and cell.",
                "initializer_fields": {},
                "key_properties": {
                    "signal_type": "enum (REQUIRED) — e.g. SignalTypeSel.Liquid_Temperature()",
                    "name": "str",
                    "connection": "int — CC number of the monitored component",
                    "mode": "enum — SignalVariableMode.EXACT()",
                    "icn1": "int — cell index within the monitored component",
                    "sub_component": "int — sub-component ID for heat structures",
                },
                "connection_slots": {},
            },
            "POWER": {
                "description": "Nuclear/electrical power source connected to heat structures.",
                "initializer_fields": {},
                "key_properties": {"name": "str"},
                "connection_slots": {},
            },
            "PLENUM": {
                "description": "Single-cell mixing plenum (simplified pipe).",
                "initializer_fields": {},
                "key_properties": {
                    "name": "str",
                    "volume": "float — plenum volume (m³)",
                    "pressure": "float — initial pressure (Pa)",
                },
                "connection_slots": {"inlet": "[JUN1] Inlet", "outlet": "[JUN2] Outlet"},
            },
            "TEE": {
                "description": "Three-way junction for flow splitting/combining.",
                "initializer_fields": {},
                "key_properties": {"name": "str"},
                "connection_slots": {"inlet": "[JUN1] Inlet", "outlet": "[JUN2] Outlet", "side": "[JUN3] Side"},
            },
        }

        schema = schemas.get(ct, {
            "description": f"{ct} component — see TRACE Users Guide for full property list.",
            "initializer_fields": {},
            "key_properties": {"name": "str"},
            "connection_slots": {},
        })
        schema["component_type"] = ct
        schema["create_method_name"] = COMPONENT_MAP[ct]["create"]
        schema["needs_initializer"] = COMPONENT_MAP[ct]["initializer"] is not None
        return schema

    @mcp.tool()
    def add_component(
        model_id: str,
        component_type: str,
        component_number: int,
        properties: dict,
        initializer: dict | None = None,
    ) -> dict:
        """Add a TRACE component to the model.

        Call get_component_schema(component_type) first to see what properties
        and initializer fields are available.

        Parameters
        ----------
        model_id : str
            Model to add the component to.
        component_type : str
            One of the TRACE component types (PIPE, FILL, BREAK, ...).
        component_number : int
            Unique integer CC number for this component type.
            Negative numbers are conventional for control blocks.
        properties : dict
            Component properties to set. Enum values as "ClassName.Method".
            Example: {"ibty": "BreakIbtySel.No_Tables", "pin": 1.5e7}
            For CONTROL_BLOCK include "control_type"; for SIGNAL_VARIABLE include "signal_type".
        initializer : dict | None
            Geometry initializer fields (for PIPE, PUMP, VESSEL, HEAT_STRUCTURE,
            VALVE, HEATER, SEPARATOR). Keys match the initializer_fields in the schema.
            Example for PIPE: {"nsegs": 10, "length": 4.0, "hd": 0.3048}

            VESSEL special key — ``ring_radii`` (list[float]):
                Outer boundary radius (m) of each ring, innermost first.
                Overrides the equal-width distribution from ``outer_radius``.
                Example for RPV with wide core + narrow downcomer annulus::

                    {"num_levels": 10, "num_rings": 2, "num_sectors": 1,
                     "outer_radius": 2.05,
                     "ring_radii": [1.8, 2.05]}

                Ring widths: dr[0]=1.8 m (core), dr[1]=0.25 m (downcomer).
        """
        model = session.get_model(model_id)

        # ring_radii is not a SNAP initializer field — extract it before create_component
        # so it doesn't land in failed_props, then apply post-creation.
        ring_radii = None
        num_sectors = None
        if component_type.upper() == "VESSEL" and initializer:
            initializer = dict(initializer)
            if "ring_radii" in initializer:
                ring_radii = initializer.pop("ring_radii")
            # num_sectors stays in the initializer (SNAP needs it for geometry),
            # but we also run a post-creation angle fixup to correct any
            # degrees-vs-radians conversion error the initializer may introduce.
            if "num_sectors" in initializer:
                num_sectors = int(initializer["num_sectors"])

        comp = create_component(model, component_type, component_number,
                                properties, initializer)
        invalidate_cc_index(model)

        if ring_radii is not None:
            _apply_ring_radii(comp, ring_radii)

        angle_fixup_ok = None
        if num_sectors is not None:
            angle_fixup_ok = _apply_sector_angles(comp, num_sectors)

        session.autosave(model_id)
        cc = _cc(comp)
        failed = getattr(comp, "_snap_mcp_failed_props", [])
        result: dict = {
            "component_type": component_type.upper(),
            "component_number": cc,
            "name": _name(comp),
            "status": "added",
        }
        warnings = [f"Property not applied: {f}" for f in failed]
        if angle_fixup_ok is False:
            warnings.append(
                "Azimuthal nodalization angle fixup unavailable — "
                "y_nodalization API not found on this SNAP build. "
                "If 'Y Angle is out of range' errors appear, use "
                "set_vessel_table(model_id, vessel_cc, 'y_nodalization', 6.2832) "
                "or a TRCIN export/import round-trip."
            )
        if warnings:
            result["warnings"] = warnings
        return result

    @mcp.tool()
    def set_component_property(
        model_id: str,
        component_type: str,
        component_number: int,
        property_name: str,
        value,
    ) -> dict:
        """Set a single property on an existing component.

        Parameters
        ----------
        model_id : str
        component_type : str
        component_number : int
        property_name : str
            Attribute name on the component (e.g. "pin", "ibty", "name").
            Nested attributes use dot notation: "fluid_segment.friction_edge_table".
        value
            Scalar, list, list-of-lists, or enum string "ClassName.Method".

        NOTE: PIPE initial conditions cannot be set via this tool — the per-cell
        IC API requires cell-by-cell assignment through fluid_segment.cells[].
        Use set_pipe_ics() instead.
        """
        model = session.get_model(model_id)
        _, comp = find_component(model, component_number)

        # Support simple dot-path traversal one level deep
        if "." in property_name:
            parts = property_name.split(".", 1)
            sub = getattr(comp, parts[0])
            set_property(sub, parts[1], value)
        else:
            set_property(comp, property_name, value)

        session.autosave(model_id)
        return {"status": "ok", "component_number": component_number,
                "property": property_name}

    @mcp.tool()
    def set_pipe_ics(
        model_id: str,
        pipe_cc: int,
        p: float,
        tl: float,
        tv: float = None,
        alp: float = 0.0,
    ) -> dict:
        """Set initial conditions on every cell of a PIPE component.

        PIPE per-cell ICs cannot be reached by set_component_property() — they
        live in fluid_segment.cells[] and require direct cell attribute assignment.
        This tool handles that correctly.

        Parameters
        ----------
        model_id : str
        pipe_cc : int
            CC number of the PIPE.
        p : float
            Pressure (Pa). Applied uniformly to all cells.
        tl : float
            Liquid temperature (K). Applied uniformly to all cells.
        tv : float | None
            Vapor temperature (K). Defaults to tl (thermodynamic equilibrium).
        alp : float
            Void fraction 0–1. Default 0.0 (single-phase liquid). Applied uniformly.

        Returns
        -------
        dict with status and number of cells written.

        Examples
        --------
        Cold leg at 15.5 MPa, 565 K, single-phase liquid::

            set_pipe_ics(model_id, 110, p=15.5e6, tl=565.0)

        Two-phase cell (10% void)::

            set_pipe_ics(model_id, 200, p=7.0e6, tl=558.0, alp=0.1)
        """
        if tv is None:
            tv = tl

        model = session.get_model(model_id)
        _, pipe = find_component(model, pipe_cc)
        cells = pipe.fluid_segment.cells
        n = len(cells)
        for i in range(n):
            c = cells[i]
            c.p   = float(p)
            c.tl  = float(tl)
            c.tv  = float(tv)
            c.alp = float(alp)

        session.autosave(model_id)
        return {
            "status": "ok",
            "pipe_cc": pipe_cc,
            "cells_written": n,
            "p_Pa": p,
            "tl_K": tl,
            "tv_K": tv,
            "alp": alp,
        }

    @mcp.tool()
    def set_vessel_table(
        model_id: str,
        vessel_cc: int,
        table_name: str,
        value,
    ) -> dict:
        """Set a 3-D property table on a VESSEL component.

        VESSEL initial conditions and edge hydraulic diameters are stored in
        Hydro3DPropertyTable objects that cannot be reached by
        set_component_property(). Use this tool instead.

        Parameters
        ----------
        model_id : str
        vessel_cc : int
            CC number of the VESSEL.
        table_name : str
            Which table to set. Cell tables (no axis suffix):
              "p"       — pressure (Pa)
              "tl"      — liquid temperature (K)
              "tv"      — vapor temperature (K)
              "alp"     — void fraction (0–1); use 0.0 for single-phase liquid
              "pa"      — non-condensable partial pressure (Pa)
              "s"       — specific entropy (J/kg·K)
            Edge tables (axis suffix required):
              "hd_axial"      — axial-edge hydraulic diameter (m)
              "hd_azimuthal"  — azimuthal-edge hydraulic diameter (m)
              "hd_radial"     — radial-edge hydraulic diameter (m)
              "frac_axial"    — axial-edge flow area fraction
              "kfac_axial"    — axial-edge loss coefficient
              ... (same _azimuthal / _radial variants available)
            Azimuthal nodalization (special):
              "y_nodalization" — per-sector azimuthal widths (radians). OPTIONAL:
                add_component already initializes a single full-circle sector
                correctly (360°), so you normally never need to set this.
                If you do, pass 2π (≈6.2832) for one full-circle sector — a value
                within rounding of a full circle is snapped to an exact 360° so it
                cannot overflow into a 'Y Angle is out of range' error. Use this
                only to override sector widths on a custom multi-sector vessel.
        value : float | list[float] | list[list[float]]
            Scalar (uniform across all cells), list of length nz (one value per
            axial level, broadcast to all planar cells), or a list of nz lists
            each of length nr*nt (full per-cell specification).

        Returns
        -------
        dict with status, dimensions set, and cells written.

        Examples
        --------
        Uniform pressure 15.5 MPa everywhere::

            set_vessel_table(model_id, 10, "p", 15.5e6)

        Per-level liquid temperature (10 levels)::

            set_vessel_table(model_id, 10, "tl",
                             [565.0, 570.0, 575.0, 580.0, 585.0,
                              590.0, 595.0, 600.0, 605.0, 610.0])

        Void fraction all zero (liquid full)::

            set_vessel_table(model_id, 10, "alp", 0.0)

        Uniform axial-edge hydraulic diameter 0.4 m::

            set_vessel_table(model_id, 10, "hd_axial", 0.4)
        """
        model = session.get_model(model_id)
        _, vessel = find_component(model, vessel_cc)

        # Special case: azimuthal (Y) nodalization — sector widths in radians.
        # Not a Hydro3DPropertyTable; requires the get_y_nodalization_cell API.
        if table_name.lower() in ("y_nodalization", "sector_angles"):
            try:
                nt = int(vessel._ntsx) if hasattr(vessel, "_ntsx") else 1
            except Exception:
                nt = 1
            # Broadcast scalar or list to per-sector values
            if isinstance(value, (int, float)):
                vals = [float(value)] * nt
            elif isinstance(value, str):
                vals = [float(value)] * nt
            elif isinstance(value, list):
                vals = [float(v) for v in value]
                if len(vals) == 1:
                    vals = vals * nt
                elif len(vals) != nt:
                    raise ValueError(
                        f"y_nodalization: expected {nt} value(s) (one per sector), "
                        f"got {len(vals)}"
                    )
            else:
                raise ValueError("value must be float or list[float]")

            # The y_nodalization_table is backed by the cell's "y_angle"
            # property, whose setter takes DEGREES (its getter returns
            # math.degrees(...)).  Callers pass azimuthal width in radians
            # (e.g. 6.2832 = 2*pi for a full circle), so convert here.
            ok = False
            try:
                import math as _math
                degs = []
                for i, v in enumerate(vals):
                    deg = _math.degrees(v)
                    # A full circle is exactly 360°.  Rounded radian inputs —
                    # notably the documented 6.2832 ≈ 2π — convert to 360.00084°,
                    # which SNAP rejects as "Y Angle is out of range".  Snap a
                    # near-full-circle value to exactly 360° so the documented
                    # value works and a good vessel isn't broken by re-setting it.
                    if abs(deg - 360.0) < 0.05:
                        deg = 360.0
                    cell = vessel.get_y_nodalization_cell(i)
                    cell.y_angle = deg
                    degs.append(deg)
                # Verify the write landed (getter returns degrees).
                chk = vessel.get_y_nodalization_cell(0).y_angle
                got = float(getattr(chk, "value", chk))
                if abs(got - degs[0]) > 1.0:
                    raise ValueError(
                        f"y_angle write did not persist (read back {got} deg, "
                        f"expected {degs[0]} deg)."
                    )
                ok = True
            except Exception as exc:
                raise ValueError(
                    f"Cannot set y_nodalization via get_y_nodalization_cell().y_angle: {exc}. "
                    "This SNAP build may not expose that API as expected."
                ) from exc

            if ok:
                session.autosave(model_id)
                return {
                    "status": "ok",
                    "vessel_cc": vessel_cc,
                    "table": table_name,
                    "sectors_written": nt,
                    "values_rad": vals,
                }

        table = _get_vessel_table(vessel, table_name)
        nz = int(table.row_count)
        nplanar = int(table.column_count)

        grid = _broadcast_vessel_value(value, nz, nplanar)

        for row_idx in range(nz):
            table[row_idx] = grid[row_idx]

        session.autosave(model_id)
        return {
            "status": "ok",
            "vessel_cc": vessel_cc,
            "table": table_name,
            "rows_written": nz,
            "cols_per_row": nplanar,
            "cells_set": nz * nplanar,
        }

    @mcp.tool()
    def set_pipe_edge_property(
        model_id: str,
        pipe_cc: int,
        edge_index: int,
        property_name: str,
        value,
    ) -> dict:
        """Set a property on a specific edge of a PIPE component.

        PIPE edges are the junctions between cells and the inlet/outlet faces.
        A pipe with N cells has N+1 edges indexed 1..N+1 (1-based).
        Edge 1 is the inlet face; edge N+1 is the outlet face.

        Common use cases:
          NFF=0 (no friction) at vessel nozzle junctions to suppress the abrupt
          area change validator; KFAC to model bends, elbows, or orifices.

        Parameters
        ----------
        model_id : str
        pipe_cc : int
        edge_index : int
            1-based. 1 = inlet face, ncells+1 = outlet face.
        property_name : str
            Edge attribute name. Most useful:
              nff    — friction flag enum. Valid values:
                         "NffSel.ConstantFric"              — wall friction only
                         "NffSel.FricAndAbrupt"             — friction + abrupt area loss
                         "NffSel.FlowFactorAndFric"         — flow factor + friction
                         "NffSel.FlowFactorFricAndAbrupt"   — flow factor + friction + abrupt
              kfac   — forward form-loss coefficient (dimensionless)
              kfacr  — reverse form-loss coefficient
              fa     — junction flow area override (m²); set intermediate area between
                       two cells to reduce the abrupt area ratio below the 2.0 limit
              hd     — junction hydraulic diameter override (m)
              abrupt — bool: flag as abrupt area change
              orifice — bool: treat as orifice
              angle  — inclination angle (degrees)
        value
            Scalar, bool, or enum string "ClassName.Method".

        Returns
        -------
        dict with status, edge_index, property, and value set.

        Examples
        --------
        Set intermediate junction flow area to reduce abrupt area ratio::

            set_pipe_edge_property(model_id, 110, 1, "fa", 0.15)

        Add forward loss coefficient on edge 3 of pipe 110::

            set_pipe_edge_property(model_id, 110, 3, "kfac", 0.5)

        Flag edge 11 as an abrupt area change::

            set_pipe_edge_property(model_id, 110, 11, "abrupt", True)
        """
        from snap_trace.type_converter import convert
        model = session.get_model(model_id)
        _, pipe = find_component(model, pipe_cc)

        edges = pipe.edges
        n_edges = len(edges)
        if edge_index < 1 or edge_index > n_edges:
            raise ValueError(
                f"edge_index={edge_index} out of range; "
                f"pipe {pipe_cc} has {n_edges} edges (1=inlet, {n_edges}=outlet)"
            )

        edge = edges[edge_index - 1]
        converted = convert(value) if isinstance(value, str) else value

        try:
            setattr(edge, property_name, converted)
        except Exception as exc:
            raise ValueError(
                f"Cannot set edge.{property_name} = {value!r}: {exc}. "
                "Valid properties: nff, kfac, kfacr, fa, hd, abrupt, orifice, angle, vl, vv"
            ) from exc

        session.autosave(model_id)
        return {
            "status": "ok",
            "pipe_cc": pipe_cc,
            "edge_index": edge_index,
            "property": property_name,
            "value": str(converted),
        }

    @mcp.tool()
    def get_pipe_edges(model_id: str, pipe_cc: int) -> dict:
        """Return the per-edge hydraulic table of a 1-D component.

        The read-side counterpart to set_pipe_edge_property(). Use this to
        review the friction and form-loss setup of an existing or imported
        model without exporting the whole TRCIN deck.

        A component with N cells has N+1 edges (1 = inlet face, N+1 = outlet
        face). For each edge this reports:
          nff     — friction flag (enum/int). 1 = wall friction on (Churchill,
                    uses epsw), no added form loss; |value| >= 100 / negative
                    flags the abrupt-area-change model (set automatically at
                    pipe-to-vessel nozzles); 0 = wall friction off.
          kfac    — forward form-loss coefficient (0 = none)
          kfacr   — reverse form-loss coefficient
          hd      — junction hydraulic diameter (m)
          fa      — junction flow area (m2)
          abrupt  — abrupt area-change flag (bool)
          orifice — orifice flag (bool)
          angle     — junction inclination. RADIANS, not degrees (retained
                      under its original name for existing callers; prefer
                      angle_rad/angle_deg, which are unambiguous).
          angle_rad — same value, explicitly radians
          angle_deg — same inclination in degrees
          grav      — the TRACE GRAV term for this junction, = sin(angle).
                      0 = horizontal, +/-1 = vertical, signed inlet -> outlet.

        On GRAV: it is a derived view of the angle, not a separate stored
        field — the plug-in's setGrav(g) writes asin(g) into edgeAngle and
        getGrav() returns sin(edgeAngle), so the two cannot disagree.  Whether
        GRAV is user-editable depends on the model's IELV setting: editable at
        IELV=0, locked read-only at IELV=1 (SNAP derives it from cell
        elevations), and hidden entirely at IELV=2.  Call get_model_options()
        to check before advising anyone to change it.

        A GRAV of exactly +1.0 or -1.0 on a pipe-to-VESSEL junction is worth a
        second look: SNAP clamps the computed ratio at 1.0, so an exact +/-1
        can mean "clamped" rather than "genuinely vertical".

        Works on any 1-D hydraulic component that exposes edges (PIPE, TEE,
        PUMP, VALVE, PLENUM). Raises if the component has no edge table.

        Parameters
        ----------
        model_id : str
        pipe_cc : int
            CC number of the component.

        Returns
        -------
        dict with component_type, pipe_cc, n_cells, n_edges, and an 'edges'
        list of per-edge dicts (edge index is 1-based; 'face' is inlet/outlet/
        interior).
        """
        model = session.get_model(model_id)
        comp_type, pipe = find_component(model, pipe_cc)

        edges = getattr(pipe, "edges", None)
        if not edges:
            raise ValueError(
                f"Component {pipe_cc} ({comp_type}) has no edge table — "
                "edges are only available on 1-D hydraulic components "
                "(PIPE, TEE, PUMP, VALVE, PLENUM)."
            )
        n_edges = len(edges)

        def _val(edge, name):
            try:
                v = getattr(edge, name)
            except Exception:
                return None
            if v is None or isinstance(v, bool):
                return v
            try:
                return float(v)
            except Exception:
                pass
            try:
                return float(v.value)
            except Exception:
                pass
            return str(v)

        rows = []
        for i, edge in enumerate(edges, start=1):
            face = "inlet" if i == 1 else "outlet" if i == n_edges else "interior"
            angle_rad = _val(edge, "angle")
            rows.append({
                "edge": i,
                "face": face,
                "nff": _val(edge, "nff"),
                "kfac": _val(edge, "kfac"),
                "kfacr": _val(edge, "kfacr"),
                "hd": _val(edge, "hd"),
                "fa": _val(edge, "fa"),
                "abrupt": _val(edge, "abrupt"),
                "orifice": _val(edge, "orifice"),
                "angle": angle_rad,
                "angle_rad": angle_rad,
                "angle_deg": _deg(angle_rad),
                "grav": _grav_from_angle(angle_rad),
            })

        return {
            "component_type": comp_type,
            "pipe_cc": pipe_cc,
            "n_cells": n_edges - 1,
            "n_edges": n_edges,
            "edges": rows,
        }

    @mcp.tool()
    def get_vessel_tables(
        model_id: str,
        vessel_cc: int,
        tables: list[str] = None,
    ) -> dict:
        """Return VESSEL per-cell IC tables and edge hydraulic-diameter tables.

        Read-side counterpart to set_vessel_table(). Use this to review whether
        a vessel's initial conditions and edge HDs were set — unset cells report
        as 'unset' (the source of "Unknown" IC errors in model check).

        Parameters
        ----------
        model_id : str
        vessel_cc : int
            CC number of the VESSEL.
        tables : list[str] | None
            Which tables to read. Default reviews the standard set:
            ["p", "tl", "tv", "alp", "hd_axial", "hd_azimuthal", "hd_radial"].
            Any valid set_vessel_table() name is accepted.

        Returns
        -------
        dict with:
          geometry : levels (nasx), rings (nrsx), sectors (ntsx), sector_angle_deg
          tables   : {name: {nz, ncols, summary, grid}}  where grid is nz rows ×
                     ncols planar cells (ncols = rings × sectors). 'summary' flags
                     uniform / range / UNSET at a glance.
        """
        model = session.get_model(model_id)
        comp_type, vessel = find_component(model, vessel_cc)
        if comp_type != "VESSEL":
            raise ValueError(f"Component {vessel_cc} is a {comp_type}, not a VESSEL.")

        names = tables or ["p", "tl", "tv", "alp",
                           "hd_axial", "hd_azimuthal", "hd_radial"]
        out = {}
        for name in names:
            try:
                table = _get_vessel_table(vessel, name)
                nz, nc, grid = _read_vessel_grid(table)
                out[name] = {
                    "nz": nz,
                    "ncols": nc,
                    "summary": _summarize_grid(grid),
                    "grid": grid,
                }
            except Exception as exc:
                out[name] = {"error": str(exc)}

        geometry = {}
        for key, attr in (("levels", "_nasx"), ("rings", "_nrsx"), ("sectors", "_ntsx")):
            try:
                geometry[key] = int(getattr(vessel, attr))
            except Exception:
                geometry[key] = None
        try:
            cell = vessel.get_y_nodalization_cell(0)
            geometry["sector_angle_deg"] = float(getattr(cell.y_angle, "value", cell.y_angle))
        except Exception:
            geometry["sector_angle_deg"] = None

        return {
            "component_type": comp_type,
            "vessel_cc": vessel_cc,
            "geometry": geometry,
            "tables": out,
        }

    @mcp.tool()
    def get_pipe_cells(model_id: str, pipe_cc: int) -> dict:
        """Return the per-cell geometry and initial conditions of a 1-D component.

        Cell-side companion to get_pipe_edges(). Reports, for each cell:
          dx   — cell length (m)
          vol  — cell volume (m3)
          p    — pressure (Pa)
          tl   — liquid temperature (K)
          tv   — vapor temperature (K)
          alp  — void fraction (0 = single-phase liquid)
          pa   — non-condensable partial pressure (Pa)
        Unset ICs report as 'unset'. Use this to review whether set_pipe_ics()
        was applied. Works on any 1-D component with a fluid_segment.

        Parameters
        ----------
        model_id : str
        pipe_cc : int
            CC number of the component.

        Returns
        -------
        dict with component_type, pipe_cc, n_cells, and a 'cells' list.
        """
        model = session.get_model(model_id)
        comp_type, pipe = find_component(model, pipe_cc)
        try:
            cells = pipe.fluid_segment.cells
        except Exception:
            raise ValueError(
                f"Component {pipe_cc} ({comp_type}) has no fluid_segment.cells — "
                "not a 1-D hydraulic component."
            )

        rows = []
        for i, c in enumerate(cells, start=1):
            rows.append({
                "cell": i,
                "dx": _attr_num(c, "dx"),
                "vol": _attr_num(c, "vol"),
                "p": _attr_num(c, "p"),
                "tl": _attr_num(c, "tl"),
                "tv": _attr_num(c, "tv"),
                "alp": _attr_num(c, "alp"),
                "pa": _attr_num(c, "pa"),
            })

        return {
            "component_type": comp_type,
            "pipe_cc": pipe_cc,
            "n_cells": len(rows),
            "cells": rows,
        }

    @mcp.tool()
    def review_model(model_id: str) -> dict:
        """Audit a model: component inventory, topology, and a flag list.

        One-shot review for an existing or imported deck. Combines:
          - component inventory (type, number, name, plus cheap per-type facts)
          - connection topology (every wired inlet/outlet/side face)
          - issues: heuristic flags for anything unset or suspicious (ICs not
            set, vessel HD tables empty/zero, dangling junctions, missing
            connection angles, pump rated values, adjacent-cell volume ratios)

        The 'issues' list is the same Python model-inspection used by
        validate_model (no file export). For the authoritative SNAP 'Check
        Model' result (Java field + system + loop-closure checks) run
        validate_model() — review_model() is the fast structural overview.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with model_id, n_components, components, connections, issues,
        issue_count, and clean (bool — True if no heuristic issues found).
        """
        from snap_trace.tools.export_tools import _python_model_check

        model = session.get_model(model_id)

        components = []
        for ctype, comp in iter_all_components(model):
            entry = {"component_type": ctype, "number": _cc(comp), "name": _name(comp)}
            try:
                if ctype == "VESSEL":
                    for key, attr in (("levels", "_nasx"), ("rings", "_nrsx"),
                                      ("sectors", "_ntsx")):
                        try:
                            entry[key] = int(getattr(comp, attr))
                        except Exception:
                            pass
                elif ctype in ("BREAK", "FILL"):
                    entry["pin"] = _attr_num(comp, "pin")
                    entry["tin"] = _attr_num(comp, "tin")
                else:
                    try:
                        entry["n_cells"] = len(comp.fluid_segment.cells)
                    except Exception:
                        pass
            except Exception:
                pass
            components.append(entry)
        components.sort(key=lambda e: (e["component_type"], e["number"]))

        connections = []
        for ctype, comp in iter_all_components(model):
            cc = _cc(comp)
            for face in ("inlet", "outlet", "side"):
                try:
                    val = getattr(comp, face, None)
                    if val is not None:
                        connections.append({
                            "component_number": cc,
                            "component_type": ctype,
                            "face": face,
                            "connection": str(val),
                        })
                except Exception:
                    pass

        # Structural heuristics review_model owns — catch obvious breakage the
        # shared _python_model_check misses (NaN/unset boundary values, dangling
        # hydraulic junctions). These were the gaps that let a clearly-broken,
        # half-wired model report 'clean'.
        def _unset(v):
            return v is None or (isinstance(v, float) and v != v)  # None or NaN

        _hydro_faces = {
            "PIPE": ("inlet", "outlet"), "PUMP": ("inlet", "outlet"),
            "VALVE": ("inlet", "outlet"), "PLENUM": ("inlet", "outlet"),
            "TEE": ("inlet", "outlet", "side"),
        }
        struct_issues = []
        for ctype, comp in iter_all_components(model):
            cc = _cc(comp)
            if ctype in ("BREAK", "FILL"):
                if _unset(_attr_num(comp, "pin")):
                    struct_issues.append(
                        f"{ctype} {cc}: boundary pressure (pin) is not set")
                if _unset(_attr_num(comp, "tin")):
                    struct_issues.append(
                        f"{ctype} {cc}: boundary temperature (tin) is not set")
            for face in _hydro_faces.get(ctype, ()):
                try:
                    val = getattr(comp, face, None)
                except Exception:
                    val = None
                if val is None or str(val).strip() in ("None", ""):
                    struct_issues.append(
                        f"{ctype} {cc}: {face} junction is not connected (dangling)")

        try:
            py_issues = _python_model_check(model)
        except Exception as exc:
            py_issues = [f"review check failed: {exc}"]

        issues = struct_issues + py_issues
        return {
            "model_id": model_id,
            "n_components": len(components),
            "components": components,
            "connections": connections,
            "issues": issues,
            "issue_count": len(issues),
            "clean": len(issues) == 0,
            "note": "Heuristic structural review. Run validate_model() for the "
                    "authoritative SNAP Check Model (Java field/system/loop-closure).",
        }

    @mcp.tool()
    def delete_component(
        model_id: str,
        component_number: int,
    ) -> dict:
        """Delete a component from the model by CC number.

        Removes the component and fires SNAP's internal cleanup (edge configs,
        sub-objects, listener notifications). Any hydraulic connections FROM other
        components TO the deleted component will be left dangling — verify with
        validate_model() after deletion and reconnect as needed.

        Use this when a component needs fundamental geometry changes (e.g. changing
        the number of axial levels in a VESSEL) that cannot be done in-place: delete
        the old component, then add_component() with the correct geometry.

        Parameters
        ----------
        model_id : str
        component_number : int
            CC number of the component to delete.

        Returns
        -------
        dict with status, component_number, and component_type of the deleted component.
        """
        model = session.get_model(model_id)
        comp_type, comp = find_component(model, component_number)
        model.delete_component(comp)
        invalidate_cc_index(model)
        session.autosave(model_id)
        return {
            "status": "deleted",
            "component_number": component_number,
            "component_type": comp_type,
        }

    @mcp.tool()
    def list_components(model_id: str) -> list[dict]:
        """List all components in the model with type, number, and name."""
        model = session.get_model(model_id)
        result = []
        for comp_type, comp in iter_all_components(model):
            result.append({
                "component_type": comp_type,
                "component_number": _cc(comp),
                "name": _name(comp),
            })
        return sorted(result, key=lambda x: (x["component_type"], x["component_number"]))

    @mcp.tool()
    def get_component(model_id: str, component_number: int) -> dict:
        """Return the component type and a summary of readable properties.

        Use this to inspect what has been set on a component before export.
        For HEAT_STRUCTURE components a 'radial_mesh' key is also returned,
        containing per-layer material names, thicknesses, and mesh point counts.
        """
        model = session.get_model(model_id)
        comp_type, comp = find_component(model, component_number)
        props = {}
        for attr in dir(comp):
            if attr.startswith("_") or attr in {"java_object", "model"}:
                continue
            try:
                val = getattr(comp, attr)
                if callable(val):
                    continue
                props[attr] = str(val)
            except Exception:
                pass
        result = {
            "component_type": comp_type,
            "component_number": component_number,
            "properties": props,
        }
        if comp_type == "HEAT_STRUCTURE":
            mesh_info = _extract_mesh_info(comp)
            if mesh_info:
                result["radial_mesh"] = mesh_info
        return result
