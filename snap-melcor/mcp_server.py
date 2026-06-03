#!/usr/bin/env python3
"""snap-melcor MCP server entry point.

Registers all snap_melcor tools with FastMCP and starts the stdio server.
Mirrors the structure of ../mcp_server.py (snap-trace).

NOT YET IMPLEMENTED — tool modules are stubs pending API investigation.
See README.md § "What needs investigation" before implementing.
"""

import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.stderr.write(
        "mcp is not installed. Install with: pip install 'mcp[cli]>=1.0'\n"
    )
    sys.exit(2)

from snap_melcor.snap_env import init_snap_env
from snap_melcor.tools.model_tools import register_model_tools
from snap_melcor.tools.component_tools import register_component_tools
from snap_melcor.tools.export_tools import register_export_tools

mcp = FastMCP("snap-melcor")

init_snap_env()
register_model_tools(mcp)
register_component_tools(mcp)
register_export_tools(mcp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
