import os
import asyncio
import json
from fastmcp import Client, FastMCP

from client_factory import ClientFactory
from mcp_paper_assistant.settings import ServerSettings


server_config = ServerSettings()
SERVER_HOST = server_config.host
SERVER_PORT = server_config.port
TRANSPORT = f"http://{SERVER_HOST}:{SERVER_PORT}/mcp"

client = Client(transport=TRANSPORT)

async def main():
    server_config = ServerSettings()
    client = ClientFactory.create_client(server_config)
    async with client:

        # Generate arguments
        # search_args = await client.call_tool("extract-user-args", {"user_query": "What's the new papers about fraud detection models?"})
        search_args = {"query": "Email classification with ML", "max_results": 3, "date_from": None}
        # print(search_args)
        
        # Execute operations
        call_tool_result = await client.call_tool("search-tool", arguments=search_args)

        papers_list = []
        for res in call_tool_result.content:
            text_res = json.loads(res.text)
            papers_list.extend(text_res["papers"])
        return papers_list


if __name__ == "__main__":
    asyncio.run(main())