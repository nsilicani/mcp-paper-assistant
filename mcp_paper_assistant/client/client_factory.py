from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

from mcp_paper_assistant.logging_config import logger
from mcp_paper_assistant.settings import ServerSettings


class ClientFactory:
    @staticmethod
    def create_client(server_config: ServerSettings) -> Client:
        """Factory method to create a FastMCP Client based on the transport."""
        transport = server_config.transport
        logger.info(f"Setting Client up with transport: {transport} ...")

        if transport == "http":
            transport_url = (
                f"http://{server_config.host}:{server_config.port}/mcp"
            )
            return Client(transport=transport_url)
        elif transport == "streamable-http":
            raise NotImplementedError(f"Not implemented for {transport}")
        elif transport == "stdio":
            PATH_TO_SERVER = Path(__file__).parent.resolve().parent / "server"
            assert PATH_TO_SERVER, f"{PATH_TO_SERVER} does not exist"
            stdio_transport = StdioTransport(
                command="python",
                args=["server.py", "--verbose"],
                env={"LOG_LEVEL": server_config.log_level.upper()},
                cwd=PATH_TO_SERVER.as_posix(),
            )
            return Client(transport=stdio_transport)
        else:
            raise ValueError(f"Unsupported transport type: {transport}")
