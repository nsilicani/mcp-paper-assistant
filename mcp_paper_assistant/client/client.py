import os
import asyncio
import json
from fastmcp.tools.tool import ToolResult

from mcp_paper_assistant.client.client_factory import ClientFactory
from mcp_paper_assistant.settings import ServerSettings
from mcp_paper_assistant.logging_config import logger


class McpClient:
    def __init__(self, server_config: ServerSettings):
        self.server_config = server_config
        self.client = ClientFactory.create_client(self.server_config)
        self.tools = []

    async def discover_tools(self):
        async with self.client:
            # Generate arguments
            search_args = {
                "query": "Email classification with ML",
                "max_results": 3,
                "date_from": None,
            }
            # Execute operations
            call_tool_result = await self.client.call_tool(
                "search-tool", arguments=search_args
            )

            papers_list = []
            for res in call_tool_result.content:
                text_res = json.loads(res.text)
                papers_list.extend(text_res["papers"])
            print(papers_list)

    async def list_tools(self):
        try:
            async with self.client:
                response = await self.client.list_tools()
                self.tools = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema,
                    }
                    for tool in response.tools
                ]
                return self.tools
        except Exception as e:
            logger.error(
                f"Server {self.server_config.name}: List tools error: {str(e)}"
            )
            return []

    async def call_tool(self, tool_name: str, arguments: dict):
        try:
            async with self.client:
                response = await self.client.call_tool(tool_name, arguments)
                return (
                    response.model_dump()
                    if hasattr(response, "model_dump")
                    else response
                )
        except Exception as e:
            logger.error(
                f"Server {self.server_config.name}: Tool call error: {str(e)}"
            )
            return {"error": str(e)}


if __name__ == "__main__":
    server_config = ServerSettings()
    mcp_client = McpClient(server_config)
    asyncio.run(mcp_client.discover_tools())
