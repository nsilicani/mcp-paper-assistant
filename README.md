# MCP Paper Assistant

## Run server
Set up environmental variables:
```env
MCP_NAME=mcp-paper-assistant
MCP_TRANSPORT=http
MPC_HOST=127.0.0.1
MCP_PORT=3031
MCP_PATH=""
MCP_LOG_LEVEL=info

ARXAIV_MAX_RESULTS=10

OPENAI_API_KEY=<your-api-key>
MODEL_MODEL=gpt-4o-2024-08-06
MODEL_TEMPERTURE=0.1

```

You can use fastmcp CLI. From project root, run:
```bash
fastmcp run .\mcp_paper_assistant\server\server.py:mcp_server
```

Note: the FastMCP CLI completely ignores the `if __name_` section, meaning that the transport needs to be provided on the command line

## Interact with Server

```bash
python .\mcp_paper_assistant\client\client.py
```

## Start the app
```bash
streamlit run app.py --browser.serverAddress localhost
```

## Resources
- [MCP inspector](https://medium.com/@laurentkubaski/how-to-use-mcp-inspector-2748cd33faeb)