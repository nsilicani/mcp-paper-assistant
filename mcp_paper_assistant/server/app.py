"""MCP server implementation with Echo tool"""

import asyncio
import os
from typing import Optional

from fastmcp import FastMCP


from mcp_paper_assistant.tools import search_paper
from mcp_paper_assistant.settings import ServerSettings
from mcp_paper_assistant.logging_config import setup_logging, logger


def create_mcp_server(server_config: Optional[ServerSettings] = None) -> FastMCP:
    """Create and configure the MCP server instance"""

    # Set up logging first
    setup_logging(server_config)

    server = FastMCP(server_config.name)

    # Register all tools with the server
    register_tools(server)

    return server


def register_tools(mcp_server: FastMCP) -> None:
    """Register all MCP tools with the server"""

    @mcp_server.tool(name="search-tool", description="Search for papers on arXiv with advanced filtering")
    def search_paper_wrapper(query: str, max_results: int, date_from: str, date_to: str):
        search_paper(query, max_results, date_from, date_to)

def main() -> None:
    if server_config is None:
        server_config = ServerSettings()

    # Create a server instance that can be imported by the MCP CLI
    mcp_server = create_mcp_server()

    # Run the server with specified transport
    mcp_server.run(
        transport=server_config.transport,
        host=server_config.host,
        port=server_config.port,
        path=server_config.path,
        log_level=server_config.log_level,
    )
