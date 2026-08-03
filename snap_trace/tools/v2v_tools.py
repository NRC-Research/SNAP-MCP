"""MCP tools: vessel-in-vessel Cartesian core VESSEL junction generation.

Wraps the NRC-Research/vessel2vessel package (the v2v library) to compute
the single-junction records that connect a Cartesian core VESSEL to the
cylindrical VESSEL it replaces, per the VESSEL-in-VESSEL modeling method.

compute_vessel_junctions() is pure computation (no Py4J/SNAP gateway) and
returns SNAP paste-format text. apply_vessel_junctions() additionally
creates the two VESSEL JUNCTION components in a live model.
"""
from __future__ import annotations

from pathlib import Path

# Axial face constants from cfnplugin.trace.components.Vessel
_FACE_POSITIVE_AXIAL = 2   # top face of the cell ("Outlet" in the GUI)
_FACE_NEGATIVE_AXIAL = -2  # bottom face of the cell ("Inlet" in the GUI)


def _require_v2v():
    try:
        import v2v  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "The vessel2vessel package is not installed in the MCP server's "
            "Python environment. Install it with:\n"
            "  pip install 'vessel2vessel @ git+https://github.com/NRC-Research/vessel2vessel@packaging'\n"
            "(requires shapely>=2.0 and numpy)."
        )


def _as_matrix(value, rows, cols, name):
    """Broadcast a scalar to a rows x cols matrix, or validate a matrix."""
    if isinstance(value, (int, float)):
        return [[float(value)] * cols for _ in range(rows)]
    if len(value) != rows or any(len(r) != cols for r in value):
        raise ValueError(
            "%s must be a scalar or a %dx%d matrix (rows x cols), got %dx%d"
            % (name, rows, cols, len(value), len(value[0]) if value else 0))
    return [[float(x) for x in r] for r in value]


def _partition_core(core_map, ring_radii, sector_angles, offset_angle):
    """Validate inputs and partition the reduced hydraulic core.

    Returns (snap_shape, areas) where snap_shape is the core map cropped
    to the assembly bounding box (values 0/1) and areas is the
    ndarray[rows, cols, rings, sectors] of overlap area fractions.
    """
    _require_v2v()
    from v2v.partitioning import (
        reduce_shape, build_sectors, build_rings, compute_partition)

    if not core_map or any(len(r) != len(core_map[0]) for r in core_map):
        raise ValueError("core_map rows must all have the same length")
    allowed = {0, 1, -1, -2}
    bad = {v for row in core_map for v in row} - allowed
    if bad:
        raise ValueError(
            "core_map may contain only 0 (empty), 1 (assembly), "
            "-1 (baffle), -2 (reflector); found %s" % sorted(bad))
    if not any(v == 1 for row in core_map for v in row):
        raise ValueError("core_map contains no hydraulic assemblies (value 1)")
    if sorted(ring_radii) != list(ring_radii):
        raise ValueError("ring_radii must be increasing (inner to outer)")
    if abs(sum(sector_angles) - 360.0) > 1e-9:
        raise ValueError("sector_angles must sum to 360 (got %r)" % (sum(sector_angles),))

    # cumulative sector angles, as the partitioning expects
    sa = [sum(sector_angles[:n + 1]) for n in range(len(sector_angles))]

    # Junction generation uses only the hydraulic cells: the core map is
    # cropped to the bounding box of the assemblies, baffles/reflectors
    # dropped. The outer ring is doubled so it fully envelops the outer
    # assemblies (the 'soft' outer boundary of the method).
    snap_shape = reduce_shape([list(r) for r in core_map])
    rows = len(snap_shape)
    cols = len(snap_shape[0])
    ring_radii = [float(r) for r in ring_radii]
    rings_safe = ring_radii[:-1] + [ring_radii[-1] * 2.0]
    sectors = build_sectors(rows, cols, sa, float(offset_angle), 1)
    rings = build_rings(rings_safe, 1)
    areas, _edges, _centroids = compute_partition(snap_shape, ring_radii, rings, sectors, 1)
    return snap_shape, areas


def _junction_records(snap_shape, areas, n_rings, n_sectors,
                      fa_matrix, dh_cart, dh_cyl, lower_limit):
    """Yield one record per single junction, in the same order and with
    the same area threshold as v2v.snapjuns.build_junctions.

    Each record: (ring, sector, x, y, area, dh) — all 1-based; y counts
    from the bottom of the Cartesian core (SNAP convention).
    """
    rows = len(snap_shape)
    cols = len(snap_shape[0])
    for r in range(rows):
        for c in range(cols):
            for rin in range(n_rings):
                for sec in range(n_sectors):
                    frac = areas[r, c, rin, sec]
                    if frac > lower_limit:
                        yield (rin + 1, sec + 1, c + 1, rows - r,
                               frac * fa_matrix[r][c],
                               min(dh_cart[r][c], dh_cyl[rin][sec]))


def compute_vessel_junctions_impl(
        core_map, ring_radii, sector_angles, offset_angle,
        cylindrical_lower_level, cylindrical_upper_level,
        cartesian_lower_level, cartesian_upper_level,
        assembly_flow_area, dh_cartesian,
        dh_cylindrical_lower, dh_cylindrical_upper,
        assembly_flow_area_upper=None, dh_cartesian_upper=None,
        min_junction_area_fraction=1e-6):
    """Compute the SNAP VESSEL junction records. See the MCP tool docstring."""
    snap_shape, areas = _partition_core(core_map, ring_radii, sector_angles, offset_angle)
    from v2v.snapjuns import build_junctions

    rows = len(snap_shape)
    cols = len(snap_shape[0])
    n_rings = len(ring_radii)
    n_sectors = len(sector_angles)

    # per-assembly data, scalars broadcast. Matrices are in the same
    # orientation as core_map (row 0 = top of the visual layout), sized to
    # the reduced hydraulic core (rows x cols).
    fa_lower = _as_matrix(assembly_flow_area, rows, cols, "assembly_flow_area")
    fa_upper = _as_matrix(
        assembly_flow_area if assembly_flow_area_upper is None else assembly_flow_area_upper,
        rows, cols, "assembly_flow_area_upper")
    dh_cart_lower = _as_matrix(dh_cartesian, rows, cols, "dh_cartesian")
    dh_cart_upper = _as_matrix(
        dh_cartesian if dh_cartesian_upper is None else dh_cartesian_upper,
        rows, cols, "dh_cartesian_upper")
    dh_cyl_lower = _as_matrix(dh_cylindrical_lower, n_rings, n_sectors, "dh_cylindrical_lower")
    dh_cyl_upper = _as_matrix(dh_cylindrical_upper, n_rings, n_sectors, "dh_cylindrical_upper")

    lower_lines, upper_lines, summary_lines, core_area, tot_juns, warnings = build_junctions(
        snap_shape, areas, n_rings, n_sectors,
        fa_lower, fa_upper,
        dh_cart_lower, dh_cart_upper, dh_cyl_lower, dh_cyl_upper,
        int(cylindrical_lower_level), int(cylindrical_upper_level),
        int(cartesian_lower_level), int(cartesian_upper_level),
        lower_limit=float(min_junction_area_fraction))

    num_assemblies = sum(v == 1 for row in snap_shape for v in row)
    return {
        "num_junctions_per_vessel_junction": tot_juns,
        "num_assemblies": num_assemblies,
        "core_area_fraction_total": core_area,
        "core_area_check": (
            "OK" if abs(core_area - num_assemblies) < 1e-6 * max(num_assemblies, 1)
            else "MISMATCH: total partitioned area %.9f != %d assemblies "
                 "(check ring_radii cover the core)" % (core_area, num_assemblies)),
        "hydraulic_core_rows": rows,
        "hydraulic_core_cols": cols,
        "warnings": [w.strip() for w in warnings],
        "lower_junction_input": "".join(lower_lines),
        "upper_junction_input": "".join(upper_lines),
        "summary": "".join(summary_lines),
    }


def _build_junction_component(model, comp_num, name,
                              source_cc, target_cc,
                              source_level, target_level, records):
    """Create one VESSEL JUNCTION component and populate its single
    junctions.

    records: iterable of (source_a, source_b, target_a, target_b, fa, dh)
    where (a, b) are the 1-based planar coordinates on each vessel —
    (ring, sector) for a cylindrical side, (x, y) for a Cartesian side.

    Ordering constraints (from the plugin source): vessels must be set
    before faces/levels (set_target_vessel resets them to defaults), and
    each single junction must be added to the component before its cell
    indices are set (the owner back-reference is installed by addSjun).
    """
    from snap.codes.trace.components import V2VConnection, V2VSingleJun

    if comp_num is not None and comp_num >= 1000:
        raise ValueError(
            "VESSEL JUNCTION component numbers must be < 1000 "
            "(junction idents are derived as number*1000+n); got %d" % comp_num)

    vj = model._create_component(V2VConnection, "Vessel Junctions", comp_num)
    jo = vj.java_object
    if name:
        vj.name = name
    vj.set_source_vessel(str(source_cc))
    vj.set_target_vessel(str(target_cc))
    # levels are 0-based in the Java model; the junction attaches to the
    # top face of the source cell and the bottom face of the target cell
    jo.setInletLocation(int(source_level) - 1)
    jo.setOutletLocation(int(target_level) - 1)
    jo.setInletFace(_FACE_POSITIVE_AXIAL)
    jo.setOutletFace(_FACE_NEGATIVE_AXIAL)

    count = 0
    for sa_, sb, ta, tb, fa, dh in records:
        elem = jo.getSjun().getClass().getComponentType().newInstance()
        jo.addSjun(-1, elem)
        entry = jo.getSjun()[count]
        sj = V2VSingleJun(model, entry)
        # tuple setter computes the planar index on the referenced vessel;
        # the axial element is carried by inlet/outlet location above
        sj.source_cell_index = (sa_, sb, 0)
        sj.target_cell_index = (ta, tb, 0)
        entry.setActiveJunction(True)
        sj.fa = float(fa)
        sj.hd = float(dh)
        count += 1

    export_ok = bool(jo.isOkayForExport(False))
    return int(jo.getComponentNumber()), count, export_ok


def apply_vessel_junctions_impl(
        model, cylindrical_vessel_cc, cartesian_vessel_cc,
        core_map, ring_radii, sector_angles, offset_angle,
        cylindrical_lower_level, cylindrical_upper_level,
        cartesian_lower_level, cartesian_upper_level,
        assembly_flow_area, dh_cartesian,
        dh_cylindrical_lower, dh_cylindrical_upper,
        assembly_flow_area_upper=None, dh_cartesian_upper=None,
        min_junction_area_fraction=1e-6,
        lower_junction_number=None, upper_junction_number=None):
    """Create both VESSEL JUNCTION components in a live model."""
    snap_shape, areas = _partition_core(core_map, ring_radii, sector_angles, offset_angle)
    rows = len(snap_shape)
    cols = len(snap_shape[0])
    n_rings = len(ring_radii)
    n_sectors = len(sector_angles)

    fa_lower = _as_matrix(assembly_flow_area, rows, cols, "assembly_flow_area")
    fa_upper = _as_matrix(
        assembly_flow_area if assembly_flow_area_upper is None else assembly_flow_area_upper,
        rows, cols, "assembly_flow_area_upper")
    dh_cart_lower = _as_matrix(dh_cartesian, rows, cols, "dh_cartesian")
    dh_cart_upper = _as_matrix(
        dh_cartesian if dh_cartesian_upper is None else dh_cartesian_upper,
        rows, cols, "dh_cartesian_upper")
    dh_cyl_lower = _as_matrix(dh_cylindrical_lower, n_rings, n_sectors, "dh_cylindrical_lower")
    dh_cyl_upper = _as_matrix(dh_cylindrical_upper, n_rings, n_sectors, "dh_cylindrical_upper")
    lim = float(min_junction_area_fraction)

    # validate the vessel nodalizations against the inputs
    cyl = model.vessel(str(cylindrical_vessel_cc))
    cart = model.vessel(str(cartesian_vessel_cc))
    cyl_r, cyl_t = int(cyl.java_object.getNrsx()), int(cyl.java_object.getNtsx())
    cart_x, cart_y = int(cart.java_object.getNrsx()), int(cart.java_object.getNtsx())
    if (cyl_r, cyl_t) != (n_rings, n_sectors):
        raise ValueError(
            "cylindrical vessel %s is %dr x %dt but inputs describe %dr x %dt"
            % (cylindrical_vessel_cc, cyl_r, cyl_t, n_rings, n_sectors))
    if (cart_x, cart_y) != (cols, rows):
        raise ValueError(
            "Cartesian vessel %s is %dx x %dy but the hydraulic core is %dx x %dy"
            % (cartesian_vessel_cc, cart_x, cart_y, cols, rows))

    # lower junction: cylindrical (top of its cell) -> Cartesian (bottom)
    lower_records = (
        (rin, sec, x, y, fa, dh)
        for rin, sec, x, y, fa, dh in _junction_records(
            snap_shape, areas, n_rings, n_sectors, fa_lower, dh_cart_lower, dh_cyl_lower, lim))
    lower_num, lower_count, lower_ok = _build_junction_component(
        model, lower_junction_number, "v2v lower",
        cylindrical_vessel_cc, cartesian_vessel_cc,
        cylindrical_lower_level, cartesian_lower_level, lower_records)

    # upper junction: Cartesian (top of its cell) -> cylindrical (bottom)
    upper_records = (
        (x, y, rin, sec, fa, dh)
        for rin, sec, x, y, fa, dh in _junction_records(
            snap_shape, areas, n_rings, n_sectors, fa_upper, dh_cart_upper, dh_cyl_upper, lim))
    upper_num, upper_count, upper_ok = _build_junction_component(
        model, upper_junction_number, "v2v upper",
        cartesian_vessel_cc, cylindrical_vessel_cc,
        cartesian_upper_level, cylindrical_upper_level, upper_records)

    num_assemblies = sum(v == 1 for row in snap_shape for v in row)
    return {
        "lower_junction": {"component_number": lower_num,
                           "single_junctions": lower_count,
                           "export_check_ok": lower_ok},
        "upper_junction": {"component_number": upper_num,
                           "single_junctions": upper_count,
                           "export_check_ok": upper_ok},
        "num_assemblies": num_assemblies,
        "hydraulic_core_rows": rows,
        "hydraulic_core_cols": cols,
    }


def register(mcp):

    @mcp.tool()
    def compute_vessel_junctions(
            core_map: list[list[int]],
            ring_radii: list[float],
            sector_angles: list[float],
            offset_angle: float,
            cylindrical_lower_level: int,
            cylindrical_upper_level: int,
            cartesian_lower_level: int,
            cartesian_upper_level: int,
            assembly_flow_area: float | list[list[float]],
            dh_cartesian: float | list[list[float]],
            dh_cylindrical_lower: float | list[list[float]],
            dh_cylindrical_upper: float | list[list[float]],
            assembly_flow_area_upper: float | list[list[float]] | None = None,
            dh_cartesian_upper: float | list[list[float]] | None = None,
            min_junction_area_fraction: float = 1e-6,
            write_files_to: str = "") -> dict:
        """Compute VESSEL junction input for a vessel-in-vessel Cartesian core.

        Implements the NRC vessel-in-vessel method: the Cartesian core
        VESSEL is coupled to the cylindrical VESSEL by two VESSEL
        junctions (one at the core bottom, one at the top), each made of
        one single junction per overlap between a Cartesian assembly
        column and a cylindrical (ring, sector) cell. This tool computes
        the geometric partitioning (via the NRC-Research/vessel2vessel
        library) and returns the junction records in SNAP's
        Connection Edge Data paste format:

            0 <TAB> r:R, t:T, z:Z <TAB> x:X, y:Y, z:Z <TAB> area <TAB> Dh <TAB> 0

        This is pure computation — no model is modified. To create the
        junction components in a live model directly, use
        apply_vessel_junctions() with the same geometry inputs.

        Parameters
        ----------
        core_map : matrix of int
            Core layout, row 0 at the top: 1 = fuel assembly, -1 = baffle,
            -2 = reflector, 0 = empty. May include the baffle/reflector
            frame; junctions are generated for the assembly cells only.
        ring_radii : list of float
            Radii of the cylindrical VESSEL rings that contain the core,
            inner to outer, in units of assembly widths. The outermost
            ring is treated as a soft boundary (its radius is internally
            doubled so it envelops all outer assemblies).
        sector_angles : list of float
            Width of each azimuthal sector in degrees (must sum to 360).
        offset_angle : float
            Angle of the start of sector 1, degrees CCW from the +x
            (3 o'clock) axis.
        cylindrical_lower_level, cylindrical_upper_level : int
            Cylindrical VESSEL axial levels the lower/upper junctions
            connect to (junctions attach to the top of the lower cell and
            the bottom of the upper cell).
        cartesian_lower_level, cartesian_upper_level : int
            Cartesian VESSEL axial levels for the lower/upper junctions.
        assembly_flow_area : float or matrix
            Assembly flow area [m^2] at the lower junction plane. A
            scalar applies to every assembly; a matrix must be sized to
            the hydraulic core (cropped to the assembly bounding box) in
            the same orientation as core_map. Junction areas are this
            value times the computed overlap area fraction.
        dh_cartesian : float or matrix
            Cartesian-side hydraulic diameter [m] at the junction planes.
        dh_cylindrical_lower, dh_cylindrical_upper : float or matrix
            Cylindrical-side hydraulic diameters [m], sized rings x
            sectors if a matrix. Each junction's Dh is the minimum of the
            Cartesian and cylindrical values.
        assembly_flow_area_upper, dh_cartesian_upper : optional
            Upper-junction-plane values; default to the lower values.
        min_junction_area_fraction : float
            Overlaps with an area fraction at or below this are dropped
            (default 1e-6).
        write_files_to : str
            Optional directory; when given, also writes
            snap_junctions_lower.dat, snap_junctions_upper.dat, and
            junction_summary.dat there.

        Returns
        -------
        dict with num_junctions_per_vessel_junction, core_area_check
        (total partitioned area must equal the assembly count),
        lower_junction_input / upper_junction_input (paste into the SNAP
        VESSEL junction Connection Edge Data dialog), and a per-assembly
        summary.
        """
        result = compute_vessel_junctions_impl(
            core_map, ring_radii, sector_angles, offset_angle,
            cylindrical_lower_level, cylindrical_upper_level,
            cartesian_lower_level, cartesian_upper_level,
            assembly_flow_area, dh_cartesian,
            dh_cylindrical_lower, dh_cylindrical_upper,
            assembly_flow_area_upper, dh_cartesian_upper,
            min_junction_area_fraction)
        if write_files_to:
            outdir = Path(write_files_to).expanduser()
            outdir.mkdir(parents=True, exist_ok=True)
            (outdir / "snap_junctions_lower.dat").write_text(result["lower_junction_input"])
            (outdir / "snap_junctions_upper.dat").write_text(result["upper_junction_input"])
            (outdir / "junction_summary.dat").write_text(result["summary"])
            result["files_written"] = [
                str(outdir / "snap_junctions_lower.dat"),
                str(outdir / "snap_junctions_upper.dat"),
                str(outdir / "junction_summary.dat"),
            ]
        return result

    @mcp.tool()
    def apply_vessel_junctions(
            model_id: str,
            cylindrical_vessel_cc: int,
            cartesian_vessel_cc: int,
            core_map: list[list[int]],
            ring_radii: list[float],
            sector_angles: list[float],
            offset_angle: float,
            cylindrical_lower_level: int,
            cylindrical_upper_level: int,
            cartesian_lower_level: int,
            cartesian_upper_level: int,
            assembly_flow_area: float | list[list[float]],
            dh_cartesian: float | list[list[float]],
            dh_cylindrical_lower: float | list[list[float]],
            dh_cylindrical_upper: float | list[list[float]],
            assembly_flow_area_upper: float | list[list[float]] | None = None,
            dh_cartesian_upper: float | list[list[float]] | None = None,
            min_junction_area_fraction: float = 1e-6,
            lower_junction_number: int | None = None,
            upper_junction_number: int | None = None) -> dict:
        """Create both vessel-in-vessel VESSEL JUNCTION components in a model.

        Computes the same partitioning as compute_vessel_junctions() and
        then builds the two VESSEL JUNCTION components directly in the
        live model — no paste-into-dialog step:

        - lower junction: cylindrical VESSEL (top face of
          cylindrical_lower_level) -> Cartesian VESSEL (bottom face of
          cartesian_lower_level)
        - upper junction: Cartesian VESSEL (top face of
          cartesian_upper_level) -> cylindrical VESSEL (bottom face of
          cylindrical_upper_level)

        Each single junction gets its source/target planar cell, flow
        area (overlap fraction x assembly flow area), and hydraulic
        diameter (min of the two sides). Friction and ICs are left at
        defaults, matching the documented workflow.

        The cylindrical vessel's rings x sectors must match
        ring_radii/sector_angles, and the Cartesian vessel's x/y cell
        counts must match the hydraulic (reduced) core — the tool
        validates both and reports a clear error on mismatch.

        VESSEL JUNCTION component numbers must be < 1000 (SNAP derives
        junction idents as number*1000+n); omit the *_junction_number
        parameters to auto-assign.

        Geometry parameters are identical to compute_vessel_junctions()
        — see that tool for their full descriptions.

        Returns
        -------
        dict with the created component numbers, per-junction single
        junction counts, and each component's export check result.
        """
        import snap_trace.session as session
        model = session.get_model(model_id)
        result = apply_vessel_junctions_impl(
            model, cylindrical_vessel_cc, cartesian_vessel_cc,
            core_map, ring_radii, sector_angles, offset_angle,
            cylindrical_lower_level, cylindrical_upper_level,
            cartesian_lower_level, cartesian_upper_level,
            assembly_flow_area, dh_cartesian,
            dh_cylindrical_lower, dh_cylindrical_upper,
            assembly_flow_area_upper, dh_cartesian_upper,
            min_junction_area_fraction,
            lower_junction_number, upper_junction_number)
        session.autosave(model_id)
        return result
