from typing import Optional

from fastmcp import FastMCP


from mcp_paper_assistant.tools import search_paper, extract_search_arguments
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
    def search_paper_wrapper(query: str, max_results: int, date_from: str | None = None, date_to: str | None = None):
        return search_paper(query, max_results, date_from, date_to)

    @mcp_server.tool(name="extract-user-args", description="Extracts structured search parameters from user input")
    def search_paper_wrapper(user_query: str,):
        return extract_search_arguments(user_query)

server_config = ServerSettings()

# Create a server instance that can be imported by the MCP CLI
mcp_server = create_mcp_server(server_config=server_config)

# Run the server with specified transport
if server_config.transport == "http":
    mcp_server.run(
        transport=server_config.transport,
        host=server_config.host,
        port=server_config.port,
        path=server_config.path,
        log_level=server_config.log_level,
    )
elif server_config.transport == "stdio":
    mcp_server.run(
        transport=server_config.transport,
    )
