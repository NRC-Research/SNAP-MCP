#!/usr/bin/env python3
"""snap-relap MCP server entry point.

Registers all snap_relap tools with FastMCP and starts the stdio server.
Mirrors the structure of ../mcp_server.py (snap-trace).
"""

import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.stderr.write(
        "mcp is not installed. Install with: pip install 'mcp[cli]>=1.0'\n"
    )
    sys.exit(2)

from snap_relap.snap_env import init_snap_env
from snap_relap.tools.model_tools import register_model_tools
from snap_relap.tools.component_tools import register_component_tools
from snap_relap.tools.export_tools import register_export_tools

mcp = FastMCP("snap-relap")

init_snap_env()
register_model_tools(mcp)
register_component_tools(mcp)
register_export_tools(mcp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
