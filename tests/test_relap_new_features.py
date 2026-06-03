#!/usr/bin/env python3
"""Test script for new snap-relap MCP tools and enhancements."""

import sys
import os

# Adjust path to find snap_relap package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "snap-relap"))

from snap_relap.snap_env import init_snap_env
from snap_relap import session as _session
from mcp.server.fastmcp import FastMCP


def run_test():
    print("Initializing SNAP environment...")
    init_snap_env()
    
    import snap.codes.relap as _rl
    print(f"SNAP RELAP version: {_rl.__file__}")
    
    # 1. Create Model
    print("\nCreating new MOD3.3 model...")
    model = _rl.new_model("MOD3.3")
    model_id = "test_model"
    _session.register(model_id, model)
    
    # Create mcp instance to register tools on for direct local calling
    mcp = FastMCP("snap-relap")
    
    from snap_relap.tools.component_tools import register_component_tools
    from snap_relap.tools.connection_tools import register_connection_tools
    from snap_relap.tools.export_tools import register_export_tools
    
    register_component_tools(mcp)
    register_connection_tools(mcp)
    register_export_tools(mcp)
    
    # Get tools from mcp tool manager
    add_comp_fn = mcp._tool_manager._tools["add_component"].fn
    get_comp_fn = mcp._tool_manager._tools["get_component"].fn
    set_prop_fn = mcp._tool_manager._tools["set_component_property"].fn
    connect_fn = mcp._tool_manager._tools["connect_components"].fn
    
    list_enums_fn = mcp._tool_manager._tools["list_enums"].fn
    get_enum_values_fn = mcp._tool_manager._tools["get_enum_values"].fn
    set_pipe_ics_fn = mcp._tool_manager._tools["set_pipe_ics"].fn
    set_pipe_geom_fn = mcp._tool_manager._tools["set_pipe_geometry"].fn
    get_schema_fn = mcp._tool_manager._tools["get_component_schema"].fn
    review_model_fn = mcp._tool_manager._tools["review_model"].fn
    validate_model_fn = mcp._tool_manager._tools["validate_model"].fn
    
    # TEST 1: Schema Tool
    print("\nTEST 1: get_component_schema...")
    schema = get_schema_fn("PIPE")
    assert "initializer_fields" in schema
    assert "key_properties" in schema
    print("Schema retrieved successfully for PIPE:", schema["description"])
    
    # TEST 2: Add Component with Properties (geometry & ICs)
    print("\nTEST 2: add_component with inline geometry/ICs for PIPE...")
    res = add_comp_fn(
        model_id=model_id,
        type="PIPE",
        cc=101,
        properties={
            "cells": 3,
            "flow_area": 0.05,
            "length": 1.2,
            "hydraulic_diameter": 0.25,
            "vertical_angle": 30.0,
            "pressure": 15.5e6,
            "temperature": 550.0,
            "void_fraction": 0.0,
            "ic_format": 3
        }
    )
    assert res["status"] == "ok"
    pipe_comp = get_comp_fn(model_id, 101)
    
    # Check that geometry and ICs were set correctly
    props = pipe_comp["properties"]
    assert "x_length" in props
    
    # Verify values set by checking float values (Java object str represents lists)
    pipes_list = list(_session.get(model_id).pipes())
    lengths = [float(x) for x in pipes_list[0].x_length]
    assert len(lengths) == 3
    assert lengths[0] == 1.2
    print("Inline geometry & IC parameters successfully applied to PIPE!")

    # TEST 3: List Enums and values
    print("\nTEST 3: list_enums and get_enum_values...")
    enums = list_enums_fn(search="Flag")
    assert "enums" in enums
    print(f"Found enums: {enums['enums']}")
    
    enum_vals = get_enum_values_fn("TDVTFlagSel")
    assert "values" in enum_vals
    assert "P_MT" in enum_vals["values"]
    print("Enum values retrieved successfully:", enum_vals["values"])
    
    # TEST 4: Bulk/broadcasting setters
    print("\nTEST 4: set_pipe_geometry and set_pipe_ics with broadcasting...")
    res = set_pipe_geom_fn(
        model_id=model_id,
        cc=101,
        flow_area=0.075,
        length=1.5,
        hydraulic_diameter=0.3,
        vertical_angle=45.0,
        wall_roughness=1.5e-5
    )
    assert res["status"] == "ok"
    
    res = set_pipe_ics_fn(
        model_id=model_id,
        cc=101,
        pressure=15.0e6,
        temperature=540.0,
        void_fraction=0.1,
        ic_format="Press_Temp_Equilib_Cond"
    )
    assert res["status"] == "ok"
    
    # Verify updated values on model
    pipes_list = list(_session.get(model_id).pipes())
    p = pipes_list[0]
    assert float(p.x_length[0]) == 1.5
    print("PIPE bulk setters with broadcasting verified successfully!")
    
    # TEST 5: Enrich enum error messages
    print("\nTEST 5: Enrich enum errors on property setting...")
    # Add a TIME_DEPENDENT_VOLUME first
    res = add_comp_fn(model_id, "TIME_DEPENDENT_VOLUME", 102, {"name": "Pressurizer-TDV"})
    assert res["status"] == "ok"
    
    res = set_prop_fn(
        model_id=model_id,
        cc=102,
        name="ic_input_format_tdv",
        value="InvalidValue"
    )
    assert res["status"] == "error"
    assert "Expected one of the values enumerated" in res["error"]
    assert "P_MT" in res["error"]
    print("Enrich enum errors verified successfully: ", res["error"])
    
    # TEST 6: Connection resolution by Name
    print("\nTEST 6: Name-based connection resolution...")
    # Add a SINGLE_JUNCTION named "SurgeLine"
    res = add_comp_fn(model_id, "SINGLE_JUNCTION", 103, {"name": "SurgeLine"})
    assert res["status"] == "ok"
    # Rename PIPE 101 to "ColdLeg"
    res = set_prop_fn(model_id, 101, "name", "ColdLeg")
    assert res["status"] == "ok"
    
    # Connect them using names instead of CC numbers
    res = connect_fn(
        model_id=model_id,
        junction_cc="SurgeLine",
        from_cc="Pressurizer-TDV",
        from_cell=1,
        to_cc="ColdLeg",
        to_cell=1
    )
    assert res["status"] == "ok"
    print("Connection by name verified successfully!")

    # TEST 7: Review model
    print("\nTEST 7: review_model topology audit...")
    review = review_model_fn(model_id)
    assert review["n_components"] == 3
    assert len(review["connections"]) == 2 # 1 inlet, 1 outlet
    print(f"Review model clean? {review['clean']}, connections: {review['connections']}")
    
    # TEST 8: Detailed validations
    print("\nTEST 8: Detailed model validation checks...")
    # Trigger mismatched flow area ratio > 10:1
    # SurgeLine junction flow_area = 0.0
    # Let's set SurgeLine flow_area to 1.0 (ColdLeg flow_area is 0.075)
    res = set_prop_fn(model_id, 103, "flow_area", 1.0)
    assert res["status"] == "ok"
    
    # Validate
    val = validate_model_fn(model_id)
    print("Validation errors:", val["errors"])
    print("Validation warnings:", val["warnings"])
    
    # Mismatched flow area should report warning
    assert any("area ratio" in w for w in val["warnings"]), "Should warn about 10:1 flow area mismatch"
    print("SUCCESS: Mismatched area ratio warning triggered successfully!")
    
    print("\nALL snap-relap NEW FEATURES TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
