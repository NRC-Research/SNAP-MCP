"""Connection-level tools for junctions and heat structures."""

from __future__ import annotations
import logging

from snap_relap import session as _session
from snap_relap.component_map import find_component

log = logging.getLogger(__name__)


def register_connection_tools(mcp) -> None:

    @mcp.tool()
    def connect_components(
        model_id: str,
        junction_cc: int,
        from_cc: int,
        from_cell: int,
        to_cc: int,
        to_cell: int,
        from_face: int = 2,  # 2 = outlet / positive
        to_face: int = 1,    # 1 = inlet / negative
    ) -> dict:
        """Connect a junction component between two volumes.

        Parameters
        ----------
        model_id : str
        junction_cc : int
            The component number of the junction (e.g. SINGLE_JUNCTION, VALVE,
            or TIME_DEPENDENT_JUNCTION).
        from_cc : int
            The source volume component number.
        from_cell : int
            The cell number in the source volume (1-based).
        to_cc : int
            The target volume component number.
        to_cell : int
            The cell number in the target volume (1-based).
        from_face : int, optional
            The connection face on the source volume (usually 2 for outlet/positive).
        to_face : int, optional
            The connection face on the target volume (usually 1 for inlet/negative).

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        
        # Format the 7-digit connection strings: {cc}{cell:02d}000{face}
        inlet_str = f"{from_cc}{from_cell:02d}000{from_face}"
        outlet_str = f"{to_cc}{to_cell:02d}000{to_face}"
        
        # Find the junction component
        ctype, comp = find_component(model, junction_cc)
        if comp is None:
            return {"status": "error", "error": f"Junction CC {junction_cc} not found in model"}
            
        try:
            # Set inlet and outlet attributes
            comp.inlet = inlet_str
            comp.outlet = outlet_str
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to set junction connection: {exc}"}

    @mcp.tool()
    def connect_heat_structure(
        model_id: str,
        hs_cc: int,
        hs_cell: int,
        face: str,
        volume_cc: int,
        volume_cell: int,
    ) -> dict:
        """Connect a heat structure cell surface to a hydraulic volume.

        Parameters
        ----------
        model_id : str
        hs_cc : int
            Heat structure component number.
        hs_cell : int
            Axial cell number in the heat structure (1-based).
        face : str
            "left" or "right" (inner or outer surface).
        volume_cc : int
            The target hydraulic volume component number.
        volume_cell : int
            The cell number in the target volume (1-based).

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        ctype, comp = find_component(model, hs_cc)
        
        if comp is None:
            return {"status": "error", "error": f"Heat structure CC {hs_cc} not found in model"}
            
        if face not in ("left", "right"):
            return {"status": "error", "error": f"Invalid face '{face}'. Must be 'left' or 'right'"}
            
        try:
            # Resolve cell index (0-based for list lookup)
            idx = hs_cell - 1
            face_list = getattr(comp, face)
            
            # Format reference value: cc * 1000000 + cell * 10000
            ref_val = volume_cc * 1000000 + volume_cell * 10000
            
            face_list[idx].bcell.reference = ref_val
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to connect heat structure: {exc}"}
