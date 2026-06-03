#!/usr/bin/env python3
"""Test script for RELAP model validation and connectivity."""

import sys
import os

# Adjust path to find snap_relap package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "snap-relap"))

from snap_relap.snap_env import init_snap_env
from snap_relap import session as _session

def run_test():
    print("Initializing SNAP environment...")
    init_snap_env()
    
    import snap.codes.relap as _rl
    print(f"SNAP RELAP version: {_rl.__file__}")
    
    # 1. Create a model
    print("\nCreating new MOD3.3 model...")
    model = _rl.new_model("MOD3.3")
    model_id = "test_model"
    _session.register(model_id, model)
    
    # 2. Add an unconnected Single Junction
    print("\nAdding unconnected SINGLE_JUNCTION component (CC 105)...")
    creator = getattr(model, "create_single_junction")
    # creator signature: area, inlet, outlet, cc
    junction = creator(0.05, None, None, 105)
    print(f"Junction CC: {junction.number}, inlet: {getattr(junction, 'inlet', None)}, outlet: {getattr(junction, 'outlet', None)}")
    
    # 3. Call validate_model logic manually
    from snap_relap.tools.export_tools import _python_model_check
    
    print("\nRunning Python model checks...")
    errors, warnings = _python_model_check(model)
    print(f"Errors found: {errors}")
    print(f"Warnings found: {warnings}")
    
    # Assertions
    assert any("105" in err and "inlet" in err for err in errors), "Should report disconnected inlet"
    assert any("105" in err and "outlet" in err for err in errors), "Should report disconnected outlet"
    print("\nSUCCESS: Python connectivity validation works as expected!")
    
    # 4. Connect component and verify errors disappear
    print("\nConnecting junction inlet and outlet...")
    # Inlet = CC 101, cell 1, face 2. Outlet = CC 102, cell 1, face 1
    junction.inlet = "101010002"
    junction.outlet = "102010001"
    
    errors, warnings = _python_model_check(model)
    print(f"Errors after connecting: {errors}")
    assert len(errors) == 0, "Errors should be cleared after connecting junction"
    print("SUCCESS: Connection state cleared errors!")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
