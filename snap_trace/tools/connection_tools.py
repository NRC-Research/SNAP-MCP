"""MCP tools: hydraulic connections and HS-fluid coupling."""
from __future__ import annotations

import snap_trace.session as session
from snap_trace.component_map import find_component, iter_all_components


def _face_is_free(comp, face) -> bool:
    """True if the component's inlet/outlet junction is unconnected."""
    try:
        v = getattr(comp, face, None)
    except Exception:
        return True
    return v is None or str(v).strip() in ("None", "")


def _resolve_target_slot(target_type: str, target_comp, provided) -> tuple[str, str | None]:
    """Auto-resolve the TARGET's junction-slot label for a 1-D connection.

    The slot in (slot, target_cc, target_cell) is the junction label on the
    TARGET component, not the source — a distinction agents reliably get wrong,
    causing InvalidFaceException loops. Resolve it so a blank/wrong slot still
    connects:
      - BREAK / FILL: single junction → always '[JUN1] Inlet'.
      - PIPE / PUMP / VALVE / TEE / PLENUM: honor a provided end if it's free,
        otherwise pick whichever end ('[JUN1] Inlet' / '[JUN2] Outlet') is free.
    Returns (slot, note) where note is a human-readable correction or None.
    """
    prov = (provided or "").strip()
    if target_type in ("BREAK", "FILL"):
        slot = "[JUN1] Inlet"
        note = None if prov == slot else f"target {target_type} has one junction; using '{slot}'"
        return slot, note
    # 1-D hydraulic target — choose a free end
    if prov == "[JUN1] Inlet" and _face_is_free(target_comp, "inlet"):
        return prov, None
    if prov == "[JUN2] Outlet" and _face_is_free(target_comp, "outlet"):
        return prov, None
    if _face_is_free(target_comp, "inlet"):
        slot = "[JUN1] Inlet"
        return slot, (f"auto-selected free target junction '{slot}'" if prov != slot else None)
    if _face_is_free(target_comp, "outlet"):
        slot = "[JUN2] Outlet"
        return slot, (f"auto-selected free target junction '{slot}'" if prov != slot else None)
    # No free junction on the target — let the original value through; the
    # caller wraps the failure with a clear message.
    return (prov or "[JUN1] Inlet"), "target has no free junction (both ends already connected)"


def register(mcp):

    @mcp.tool()
    def connect_components(
        model_id: str,
        component_number: int,
        face: str,
        target_junction_slot: str,
        target_component_number: int,
        target_cell_index: int = 1,
        angle_deg: float = 0.0,
    ) -> dict:
        """Connect two 1-D TRACE components via a hydraulic junction.

        This mirrors the standpipe.py pattern::

            break_11.inlet = ("[JUN2] Outlet", 21, 20)
            pipe_21.inlet  = ("[JUN1] Inlet",   1,  1)

        CRITICAL: NEVER pass a VESSEL CC as component_number OR target_component_number.
        Using a VESSEL on either side crashes the MEBatch JVM — VESSEL junctions use
        geometry-specific face labels ("Positive Azimuthal", etc.) that are incompatible
        with the "inlet"/"outlet" setattr this tool uses. Use connect_pipe_to_vessel()
        for any pipe-to-VESSEL connection — no exceptions.

        Parameters
        ----------
        model_id : str
        component_number : int
            The component whose face is being connected (the "left" side).
            Must be a 1-D component (PIPE, FILL, BREAK, PUMP, VALVE, TEE, PLENUM).
        face : str
            Which face on component_number to connect.
            Typical values: "inlet", "outlet".
        target_junction_slot : str
            Junction label on the TARGET component. AUTO-RESOLVED — pass ""
            (or any guess) and the correct slot is chosen for you:
              target BREAK / FILL  → "[JUN1] Inlet"  (single junction)
              target PIPE/PUMP/VALVE/TEE/PLENUM → the target's free end
                ("[JUN1] Inlet" if its inlet is free, else "[JUN2] Outlet")
            A wrong value is corrected automatically; the slot actually used is
            returned, with a 'slot_note' when it differs from what you passed.
            If the target has NO free junction (e.g. a pipe already connected on
            both ends), the call returns a clear error instead of looping.
        target_component_number : int
            The CC number of the 1-D component to connect to.
            Do NOT pass a VESSEL CC here — use connect_pipe_to_vessel() instead.
        target_cell_index : int
            Which cell of the target to attach to.
            Use 1 for the first cell and the component's ncells for the last.
        angle_deg : float
            Connection angle in DEGREES relative to horizontal (DANGLE in TRCIN).
            0° = horizontal flow (e.g. horizontal cold/hot leg). 90° = upward vertical.
            -90° = downward vertical. MUST be set — SNAP model check reports
            "Connection Angle has not been set" if this is missing.
            Default: 0.0 (horizontal). Adjust for non-horizontal connections.

        Returns
        -------
        dict confirming the connection.

        Examples
        --------
        Connect pipe 21's inlet to fill 1 at cell 1::

            connect_components(model_id, 21, "inlet", "[JUN1] Inlet", 1, 1)

        Connect pipe 21's outlet to break 11 at cell 20::

            connect_components(model_id, 11, "inlet", "[JUN2] Outlet", 21, 20)

        Connect pump 51 inlet from fill 1, outlet to pipe 21 cell 1::

            connect_components(model_id, 51, "inlet",  "[JUN1] Inlet",  1,  1)
            connect_components(model_id, 51, "outlet", "[JUN2] Outlet", 21, 1)

        Vertical riser (upward flow, 90°)::

            connect_components(model_id, 30, "outlet", "[JUN2] Outlet", 40, 1, angle_deg=90.0)
        """
        model = session.get_model(model_id)

        # Guard: reject VESSEL on either side before the Java call.
        # setattr("outlet"/"inlet") on a VESSEL Python wrapper silently creates a
        # Python attribute (no Java call), so the connection appears to succeed but
        # is never actually made.
        #
        # Three-layer check (most to least authoritative):
        #   1. Direct vessel CC scan — iterate model.vessels() to match by CC number.
        #      This bypasses find_component's iteration-order dependency and handles
        #      the case where vessel.java_object.getCCnumber() fails silently so the
        #      vessel is skipped and find_component returns a wrong type (e.g. TRIP).
        #   2. Type string from find_component.
        #   3. Java class name on the returned comp object.
        def _vessel_ccs(mdl) -> set[int]:
            """Return the set of CC numbers belonging to VESSEL components."""
            ccs: set[int] = set()
            try:
                from snap_trace.component_map import _coerce_list as _cl
                for v in _cl(mdl.vessels()):
                    for attr in ("cc_number", "_cc_number"):
                        try:
                            ccs.add(int(getattr(v, attr)))
                            break
                        except Exception:
                            pass
                    try:
                        ccs.add(int(v.java_object.getCCnumber()))
                    except Exception:
                        pass
            except Exception:
                pass
            return ccs

        vessel_ccs = _vessel_ccs(model)

        def _is_vessel(comp_obj, type_str, cc: int) -> bool:
            if cc in vessel_ccs:
                return True
            if type_str == "VESSEL":
                return True
            try:
                cls = comp_obj.java_object.getClass().getName()
                return "VesselComponent" in cls or "Vessel" in cls.split(".")[-1]
            except Exception:
                return False

        source_type, comp = find_component(model, component_number)
        if _is_vessel(comp, source_type, component_number):
            raise ValueError(
                f"connect_components() cannot use a VESSEL as source (CC {component_number}). "
                "Use connect_pipe_to_vessel() instead — VESSEL junctions use geometry-specific "
                "face labels ('Positive Azimuthal', etc.) that 1-D tools cannot set."
            )
        target_type, tgt = find_component(model, target_component_number)
        if _is_vessel(tgt, target_type, target_component_number):
            raise ValueError(
                f"connect_components() cannot target a VESSEL (CC {target_component_number}). "
                "Use connect_pipe_to_vessel() instead — VESSEL junctions use geometry-specific "
                "face labels ('Positive Azimuthal', etc.) that 1-D tools cannot set."
            )

        # Auto-resolve the target junction slot so a blank/wrong label still
        # connects (agents reliably pass the wrong slot — it's the TARGET's
        # junction, not the source's — which caused InvalidFaceException loops).
        resolved_slot, slot_note = _resolve_target_slot(target_type, tgt, target_junction_slot)
        try:
            setattr(comp, face, (resolved_slot, target_component_number, target_cell_index))
        except Exception as exc:
            # The gateway is healthy (this is a Java-side modeling error). Return
            # an actionable message instead of a raw Py4J trace so the agent can
            # self-correct rather than loop.
            free = [f for f in ("inlet", "outlet") if _face_is_free(tgt, f)]
            if free:
                hint = (f"Target {target_type} {target_component_number} free "
                        f"junction(s): {free}.")
            else:
                hint = (f"Target {target_type} {target_component_number} has NO free "
                        "junction — both ends are already connected. A pipe cannot "
                        "connect both ends to the same target; check you have not "
                        "connected this pipe to the vessel on both inlet and outlet.")
            raise ValueError(
                f"Could not connect {source_type} {component_number} '{face}' to "
                f"{target_type} {target_component_number}: {exc} {hint}"
            ) from None

        # Set junction angle (DANGLE) — required by SNAP model check
        angle_set = False
        try:
            jun = getattr(comp, face)
            for angle_attr in ("angle", "dangle", "theta", "con_angle"):
                try:
                    setattr(jun, angle_attr, float(angle_deg))
                    angle_set = True
                    break
                except Exception:
                    pass
        except Exception:
            pass

        session.autosave(model_id)
        result = {
            "status": "connected",
            "from_component": component_number,
            "face": face,
            "target_junction_slot": resolved_slot,
            "target_component": target_component_number,
            "target_cell": target_cell_index,
            "angle_deg": angle_deg,
            "angle_set": angle_set,
        }
        if slot_note:
            result["slot_note"] = slot_note
        return result

    @mcp.tool()
    def connect_pipe_to_vessel(
        model_id: str,
        pipe_cc: int,
        pipe_face: str,
        vessel_cc: int,
        vessel_level: int,
        vessel_ring: int = 1,
        vessel_sector: int = 1,
        vessel_face: str = "Positive Azimuthal",
        auto_nff: bool = True,
    ) -> dict:
        """Connect a 1-D hydraulic component to a VESSEL cell.

        Use this instead of connect_components() when the target is a VESSEL.
        The SNAP VESSEL API requires geometry-specific face labels ("Positive
        Azimuthal", "Negative Azimuthal", etc.); the 1-D labels used by
        connect_components() are rejected and cause a silent connection failure.

        The VESSEL cell is addressed by human-readable (level, ring, sector)
        coordinates. The flat cell index is computed internally:

            cell = (level - 1) * (nr × nt) + (ring - 1) × nt + (sector - 1) + 1

        where nr = num_rings and nt = num_sectors are read from the vessel.

        Parameters
        ----------
        model_id : str
        pipe_cc : int
            CC number of the 1-D component (PIPE, FILL, BREAK, PUMP, VALVE, etc.)
        pipe_face : str
            Face on the 1-D component to wire: "inlet" or "outlet".
        vessel_cc : int
            CC number of the VESSEL component.
        vessel_level : int
            1-based axial level on the vessel (1 = bottom / lowest level).
        vessel_ring : int
            1-based radial ring (1 = innermost ring). Default 1.
        vessel_sector : int
            1-based azimuthal sector (1 = first sector). Default 1.
        vessel_face : str
            Face of the vessel cell the pipe attaches to.
            Cylindrical geometry (RPV):
              "Positive Azimuthal"  — default; standard for external pipe nozzles
              "Negative Azimuthal"  — for a second pipe at the same level/ring
              "Positive Radial"
              "Negative Radial"
            Cartesian geometry:
              "Positive X Axis", "Negative X Axis"
              "Positive Y Axis", "Negative Y Axis"
        auto_nff : bool
            If True (default), automatically set NffSel.FricAndAbrupt on the
            pipe edge that connects to the vessel.  Pipe-to-vessel junctions
            always have an area change, so SNAP's abrupt-area validator fires
            unless NFF=FricAndAbrupt (or FricAndAbrupt variant) is set on
            that edge.  Disable only if you intend to set NFF manually via
            set_pipe_edge_property().

        Returns
        -------
        dict with status, coordinates used, and the computed flat cell index.

        Examples
        --------
        Cold leg pipe 110 outlet → VESSEL 10, outer ring (ring 2), top level (10)::

            connect_pipe_to_vessel(model_id, 110, "outlet", 10, 10, vessel_ring=2)

        Hot leg pipe 210 inlet ← VESSEL 10, inner ring (ring 1), top level (10)::

            connect_pipe_to_vessel(model_id, 210, "inlet", 10, 10, vessel_ring=1)

        Second cold leg 120 outlet → same level but negative azimuthal face::

            connect_pipe_to_vessel(model_id, 120, "outlet", 10, 10,
                                   vessel_ring=2, vessel_face="Negative Azimuthal")
        """
        model = session.get_model(model_id)

        _, hydro_comp = find_component(model, pipe_cc)
        _, vessel = find_component(model, vessel_cc)

        try:
            nr = int(vessel._nrsx)
        except Exception:
            nr = 1
        try:
            nt = int(vessel._ntsx)
        except Exception:
            nt = 1

        if vessel_ring < 1 or vessel_ring > nr:
            raise ValueError(
                f"vessel_ring={vessel_ring} out of range; vessel has {nr} ring(s)"
            )
        if vessel_sector < 1 or vessel_sector > nt:
            raise ValueError(
                f"vessel_sector={vessel_sector} out of range; vessel has {nt} sector(s)"
            )

        flat_cell = (
            (vessel_level - 1) * (nr * nt)
            + (vessel_ring - 1) * nt
            + (vessel_sector - 1)
            + 1
        )

        setattr(hydro_comp, pipe_face, (vessel_face, vessel_cc, flat_cell))

        # Auto-set NffSel.FricAndAbrupt on the connecting pipe edge so the
        # abrupt-area-change validator doesn't fire on every vessel connection.
        nff_edge_index = None
        if auto_nff:
            try:
                import snap.codes.trace.enums as _enums
                nff_val = _enums.NffSel.FricAndAbrupt()
                edges = hydro_comp.edges
                n_edges = len(edges)
                ei = 0 if pipe_face == "inlet" else n_edges - 1
                edges[ei].nff = nff_val
                nff_edge_index = ei + 1  # 1-based for result
            except Exception:
                pass

        session.autosave(model_id)
        result = {
            "status": "connected",
            "pipe_cc": pipe_cc,
            "pipe_face": pipe_face,
            "vessel_cc": vessel_cc,
            "vessel_level": vessel_level,
            "vessel_ring": vessel_ring,
            "vessel_sector": vessel_sector,
            "vessel_face": vessel_face,
            "flat_cell_index": flat_cell,
        }
        if nff_edge_index is not None:
            result["nff_set"] = f"FricAndAbrupt on edge {nff_edge_index}"
        elif auto_nff:
            result["nff_warning"] = (
                "auto_nff=True but NffSel.FricAndAbrupt could not be set — "
                "set manually via set_pipe_edge_property()"
            )
        return result

    @mcp.tool()
    def get_connections(model_id: str) -> list[dict]:
        """Return all connection information visible on each component.

        Inspects inlet/outlet attributes of every hydraulic component to
        build a topology summary.
        """
        model = session.get_model(model_id)
        connections = []
        for comp_type, comp in iter_all_components(model):
            cc = _cc(comp)
            for face in ("inlet", "outlet", "side"):
                try:
                    val = getattr(comp, face, None)
                    if val is not None:
                        connections.append({
                            "component_number": cc,
                            "component_type": comp_type,
                            "face": face,
                            "connection": str(val),
                        })
                except Exception:
                    pass
        return connections

    @mcp.tool()
    def check_loop_closure(model_id: str) -> dict:
        """Run SNAP's native loop closure check in headless mode.

        Uses TraceModel.getHeadlessLoopClosureErrors() — the same elevation/
        loop arithmetic as the GUI Loop Check — without requiring MessageWindow
        or a Swing display. Requires the headless-validation build of trace.jar.

        The loop closure check verifies that the net elevation change around
        every closed hydraulic circuit is zero (within tolerance). Errors look
        like: "Loop starting at Pipe 110: elevation error = 0.35 m (tolerance
        0.001 m)".  These errors are distinct from connection errors — a model
        can be fully wired but still fail loop closure if component elevations
        are geometrically inconsistent.

        Parameters
        ----------
        model_id : str

        Returns
        -------
        dict with:
            closed  : bool       — True when no loop closure errors found
            errors  : list[str]  — one string per loop closure violation
            source  : str        — "snap_native" when JAR method is available,
                                   "unavailable" if the JAR predates this feature
        """
        model = session.get_model(model_id)
        try:
            raw = model.java_model.getHeadlessLoopClosureErrors()
            errors = list(raw) if raw is not None else []
            return {
                "closed": len(errors) == 0,
                "errors": errors,
                "source": "snap_native",
            }
        except Exception as exc:
            return {
                "closed": None,
                "errors": [],
                "source": "unavailable",
                "detail": (
                    f"getHeadlessLoopClosureErrors() not available: {exc}. "
                    "Deploy the headless-validation trace.jar to /opt/snap/plugins/."
                ),
            }


    @mcp.tool()
    def connect_heat_structure(
        model_id: str,
        hs_number: int,
        hs_axial_cell: int,
        face: str,
        hydro_cc: int,
        hydro_cell: int,
    ) -> dict:
        """Wire one axial cell surface of a HEAT_STRUCTURE to a hydraulic component cell.

        Sets the HTFF (hydraulic coupling) boundary condition on the chosen
        surface and records which hydraulic cell it faces. Call once per
        (hs_cell, face) pair — i.e. up to 2 × n_axial times per HS.

        Parameters
        ----------
        model_id : str
        hs_number : int
            CC number of the HEAT_STRUCTURE.
        hs_axial_cell : int
            1-based axial cell index of the heat structure (1 = bottom/inlet end).
        face : str
            "inner" or "outer".
        hydro_cc : int
            CC number of the hydraulic component (PIPE, PLENUM, etc.) to couple to.
        hydro_cell : int
            1-based cell index within that hydraulic component.

        Returns
        -------
        dict confirming the coupling.

        Example — HS 900 upflow tube bundle, 2 axial cells::

            connect_heat_structure(model_id, 900, 1, "inner", 10, 1)
            connect_heat_structure(model_id, 900, 2, "inner", 10, 2)
            connect_heat_structure(model_id, 900, 1, "outer", 20, 1)
            connect_heat_structure(model_id, 900, 2, "outer", 20, 2)
        """
        model = session.get_model(model_id)
        _, hs = find_component(model, hs_number)
        comp_type, hydro_comp = find_component(model, hydro_cc)

        cells = hs.cells
        cell = cells[hs_axial_cell - 1]
        surface = getattr(cell, face)  # Surface object

        # idbc=2 → HTFF coupling to a hydraulic component
        surface.idbc = 2

        # CellReference coupling differs for VESSEL vs 1-D components.
        #
        # For 1-D components (PIPE, PLENUM, etc.):
        #   hcom.reference = cc * 1000 + hydro_cell (1-based)  ← standard encoding
        #
        # For VESSEL:
        #   setReferencedCellID(cc*1000 + flat_cell) is broken — CellReconnector
        #   decodes the integer as (within_level_0based, axial_level_0based) not
        #   as a flat sequential cell index, causing ArrayIndexOutOfBoundsException.
        #   The correct path is to call setHydroRef / setCellRef directly on the
        #   Java CellReference object, bypassing the packed-integer encoding.
        #   getCellAt(flat_0based) uses the single-arg overload which correctly
        #   computes level = flat // (nr*nt) and within = flat % (nr*nt).
        if comp_type == "VESSEL":
            hcom_j = surface.hcom.java_object
            vessel_j = hydro_comp.java_object
            flat_0based = hydro_cell - 1  # hydro_cell is 1-based
            cell_j = vessel_j.getCellAt(flat_0based)
            hcom_j.setHydroRef(vessel_j)
            hcom_j.setCellRef(cell_j)
        else:
            surface.hcom.reference = hydro_cc * 1000 + hydro_cell

        session.autosave(model_id)
        return {
            "status": "connected",
            "hs": hs_number,
            "hs_cell": hs_axial_cell,
            "face": face,
            "hydro_cc": hydro_cc,
            "hydro_cell": hydro_cell,
        }


def _cc(comp) -> int:
    try:
        return int(comp.java_object.getCCnumber())
    except Exception:
        return -1
