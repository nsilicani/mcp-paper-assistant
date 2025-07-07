"""MCP server package initialization"""

from mcp_paper_assistant.settings import load_settings
from mcp_paper_assistant.server.app import create_mcp_server

# Create server instance with default configuration
server = create_mcp_server(load_settings())

__all__ = ["server", "create_mcp_server"]
