"""Connection-level tools for junctions and heat structures."""

from __future__ import annotations
import logging

from snap_relap import session as _session
from snap_relap.component_map import find_component

log = logging.getLogger(__name__)


def find_component_by_id_or_name(model, identifier: int | str):
    """Find a component by its CC number (if int or digit string) or by its name."""
    if isinstance(identifier, int):
        return find_component(model, identifier)
    if isinstance(identifier, str):
        if identifier.isdigit():
            return find_component(model, int(identifier))
        
        # Search by name (handle 8-char truncation limit for RELAP names)
        target_name = identifier.strip()
        if len(target_name) > 8:
            target_name = target_name[:8]

        from snap_relap.component_map import COMPONENT_MAP, _coerce_list
        for ctype, cfg in COMPONENT_MAP.items():
            try:
                getter = getattr(model, cfg["list"])
                items = _coerce_list(getter())
                for item in items:
                    try:
                        if str(item.name).strip() == target_name:
                            # Find the CC number
                            cc = -1
                            for attr in ("getCCnumber", "number", "getComponentNumber"):
                                try:
                                    v = getattr(item, attr)
                                    cc = int(v() if callable(v) else v)
                                    break
                                except Exception:
                                    pass
                            return ctype, item, cc
                    except Exception:
                        pass
            except Exception:
                pass
    return None, None, -1


def resolve_cc(model, identifier: int | str) -> int:
    """Helper to resolve identifier to CC number."""
    if isinstance(identifier, int):
        return identifier
    if isinstance(identifier, str):
        if identifier.isdigit():
            return int(identifier)
        # Search by name
        _, _, cc = find_component_by_id_or_name(model, identifier)
        return cc
    return -1


def register_connection_tools(mcp) -> None:

    @mcp.tool()
    def connect_components(
        model_id: str,
        junction_cc: int | str,
        from_cc: int | str,
        from_cell: int,
        to_cc: int | str,
        to_cell: int,
        from_face: int = 2,  # 2 = outlet / positive
        to_face: int = 1,    # 1 = inlet / negative
    ) -> dict:
        """Connect a junction component between two volumes.

        Parameters
        ----------
        model_id : str
        junction_cc : int or str
            The component number or name of the junction.
        from_cc : int or str
            The source volume component number or name.
        from_cell : int
            The cell number in the source volume (1-based).
        to_cc : int or str
            The target volume component number or name.
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
        
        # Resolve CC numbers from names if given
        j_cc = resolve_cc(model, junction_cc)
        f_cc = resolve_cc(model, from_cc)
        t_cc = resolve_cc(model, to_cc)

        if j_cc == -1:
            return {"status": "error", "error": f"Junction '{junction_cc}' not found"}
        if f_cc == -1:
            return {"status": "error", "error": f"Source volume '{from_cc}' not found"}
        if t_cc == -1:
            return {"status": "error", "error": f"Target volume '{to_cc}' not found"}

        # Format the connection strings: {cc:03d}{cell:02d}000{face} (9-digit RELAP5 format)
        inlet_str = f"{f_cc:03d}{from_cell:02d}000{from_face}"
        outlet_str = f"{t_cc:03d}{to_cell:02d}000{to_face}"
        
        # Find the junction component
        ctype, comp = find_component(model, j_cc)
        if comp is None:
            return {"status": "error", "error": f"Junction CC {j_cc} not found in model"}
            
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
        hs_cc: int | str,
        hs_cell: int,
        face: str,
        volume_cc: int | str,
        volume_cell: int,
    ) -> dict:
        """Connect a heat structure cell surface to a hydraulic volume.

        Parameters
        ----------
        model_id : str
        hs_cc : int or str
            Heat structure component number or name.
        hs_cell : int
            Axial cell number in the heat structure (1-based).
        face : str
            "left" or "right" (inner or outer surface).
        volume_cc : int or str
            The target hydraulic volume component number or name.
        volume_cell : int
            The cell number in the target volume (1-based).

        Returns
        -------
        dict with keys: status (str)
        """
        model = _session.get(model_id)
        
        # Resolve CC numbers from names if given
        h_cc = resolve_cc(model, hs_cc)
        v_cc = resolve_cc(model, volume_cc)

        if h_cc == -1:
            return {"status": "error", "error": f"Heat structure '{hs_cc}' not found"}
        if v_cc == -1:
            return {"status": "error", "error": f"Volume '{volume_cc}' not found"}

        ctype, comp = find_component(model, h_cc)
        if comp is None:
            return {"status": "error", "error": f"Heat structure CC {h_cc} not found in model"}
            
        if face not in ("left", "right"):
            return {"status": "error", "error": f"Invalid face '{face}'. Must be 'left' or 'right'"}
            
        try:
            # Resolve cell index (0-based for list lookup)
            idx = hs_cell - 1
            face_list = getattr(comp, face)
            
            # Format reference value: cc * 1000000 + cell * 10000
            ref_val = v_cc * 1000000 + volume_cell * 10000
            
            face_list[idx].bcell.reference = ref_val
            return {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": f"Failed to connect heat structure: {exc}"}
