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
    from snap_relap.tools.model_tools import register_model_tools
    
    register_component_tools(mcp)
    register_connection_tools(mcp)
    register_export_tools(mcp)
    register_model_tools(mcp)
    
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
    
    # TEST 9: Bulk Property Setting and Component Deletion
    print("\nTEST 9: Bulk setting and delete_component...")
    set_bulk_fn = mcp._tool_manager._tools["set_properties_bulk"].fn
    delete_comp_fn = mcp._tool_manager._tools["delete_component"].fn
    
    # Bulk set hydraulic diameter on ColdLeg and SurgeLine
    res = set_bulk_fn(model_id, [101, 103], "hydraulic_diameter", 0.35)
    assert res["status"] == "ok"
    
    # Verify via get
    coldleg_data = get_comp_fn(model_id, 101)
    # hydraulic_diameter is list for PIPE
    assert 0.35 in coldleg_data["properties"]["hydraulic_diameter"]
    
    # Add a dummy component and delete it
    res = add_comp_fn(model_id, "SINGLE_VOLUME", 999, {"name": "DummyVol"})
    assert res["status"] == "ok"
    
    res = delete_comp_fn(model_id, 999)
    assert res["status"] == "ok"
    # Ensure it is gone
    dummy = get_comp_fn(model_id, 999)
    assert dummy["status"] == "error"
    print("Bulk setting and component deletion verified successfully!")

    # TEST 10: Setting Table Data (tdv_data)
    print("\nTEST 10: Setting TDV table data...")
    # Add a TDV
    res = add_comp_fn(model_id, "TIME_DEPENDENT_VOLUME", 104, {"name": "TDV104"})
    assert res["status"] == "ok"
    
    # Set tdv_data table (Time, Pressure, Temperature)
    table_data = [
        [0.0, 1.5e7, 550.0],
        [10.0, 1.5e7, 550.0],
        [100.0, 1.5e7, 550.0]
    ]
    res = set_prop_fn(model_id, 104, "tdv_data", table_data)
    assert res["status"] == "ok"
    
    # Check that tdv_data was set and is returned as list of lists by get_component
    comp_data = get_comp_fn(model_id, 104)
    tdv_prop = comp_data["properties"]["tdv_data"]
    assert isinstance(tdv_prop, list)
    assert len(tdv_prop) == 3
    assert tdv_prop[0][0] is None or str(tdv_prop[0][0]) == "None"
    assert float(tdv_prop[0][1]) == 0.0
    assert float(tdv_prop[1][2]) == 1.5e7
    print("Table data setting (tdv_data) and serialization verified successfully!")

    # TEST 11: Auto-set format for SINGLE_VOLUME
    print("\nTEST 11: Auto-set ic_input_format for SINGLE_VOLUME...")
    res = add_comp_fn(model_id, "SINGLE_VOLUME", 105, {"name": "Vol105", "temperature": 500.0})
    assert res["status"] == "ok"
    
    comp_data = get_comp_fn(model_id, 105)
    ic_fmt = comp_data["properties"]["ic_input_format"]
    assert str(ic_fmt) == "3" or int(ic_fmt) == 3 or "equilib" in str(ic_fmt).lower()
    
    # Verify helpful error message when setting disabled property
    res = set_prop_fn(model_id, 105, "ic_input_format", "CellICFormatSelEditorv.Press_Liq_E_Vap_E_Void_Frac")
    assert res["status"] == "ok"
    # Now temperature is disabled, setting it should fail with a helpful error explaining the format dependency
    res = set_prop_fn(model_id, 105, "temperature", 510.0)
    assert res["status"] == "error"
    assert "is disabled. You must set 'ic_input_format' to 3" in res["error"]
    print("Auto-set format dependencies and rich error feedback verified successfully!")

    # TEST 12: export_relap and import post-patching
    print("\nTEST 12: export_relap and import_relap post-patching...")
    export_fn = mcp._tool_manager._tools["export_relap"].fn
    import_fn = mcp._tool_manager._tools["import_relap"].fn
    import tempfile
    
    # Let's delete the temporary test component 105 to clean up the model
    delete_comp_fn = mcp._tool_manager._tools["delete_component"].fn
    delete_comp_fn(model_id, 105)
    
    # Let's fix SurgeLine hydraulic diameter to make model valid for export
    res = set_prop_fn(model_id, 103, "hydraulic_diameter", 0.3)
    assert res["status"] == "ok"
    # Also set table data for Pressurizer-TDV to resolve its validation error
    res = set_prop_fn(model_id, 102, "tdv_data", table_data)
    assert res["status"] == "ok"
    
    with tempfile.NamedTemporaryFile(suffix=".inp", delete=False) as f:
        tmp_inp = f.name
        
    try:
        # Export model (verifies path conversion)
        res = export_fn(model_id, tmp_inp, force=True)
        print("Export relap response:", res)
        assert res["status"] == "ok"
        
        # Import the model back (verifies junction patching)
        import_res = import_fn(tmp_inp)
        assert import_res["status"] == "ok"
        new_model_id = import_res["model_id"]
        
        # Verify imported junction has its connections wired
        junc_data = get_comp_fn(new_model_id, 103)
        assert junc_data["properties"]["inlet"] == "102010002"
        assert junc_data["properties"]["outlet"] == "101010001"
        print("Model export string path and import junction post-patching verified successfully!")
    finally:
        if os.path.exists(tmp_inp):
            os.unlink(tmp_inp)

    print("\nALL snap-relap NEW FEATURES TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
