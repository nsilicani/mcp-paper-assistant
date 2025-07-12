import requests

# Define the SSE endpoint and payload
url = "http://localhost:3001/mcp/"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

# Send the POST initializing request
req_id = 1
data = {
    "jsonrpc": "2.0",
    "id": req_id,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "curl", "version": "8.x"},
    },
}
response = requests.post(url, headers=headers, json=data, stream=True)

# Store session id
session_id = response.headers.get("mcp-session-id")

# Update request headers with session ID
updated_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "Mcp-Session-Id": session_id,
}
req_id += 1

# Send the POST notification request for initialization complete
notify_initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}
notify_response = requests.post(
    url=url,
    headers=updated_headers,
    json=notify_initialized,
    stream=True,
)
print(f"Init Notification Response: {notify_response=}")
print(notify_response.text)
req_id += 1

# Send POST request to list tools
payload_for_tools_list = {
    "jsonrpc": "2.0",
    "id": req_id,
    "method": "tools/list",
}
response_tools_list = requests.post(
    url=url,
    headers=updated_headers,
    json=payload_for_tools_list,
    stream=True,
)
print(f"Tools List Response: {response_tools_list=}")
print(response_tools_list.text)
req_id += 1

# Send POST request to call tool
payload_for_tool_call = {
    "jsonrpc": "2.0",
    "id": req_id,
    "method": "tools/call",
    "params": {"name": "echo", "arguments": {"text": "Hello World!"}},
}
response_tool_call = requests.post(
    url=url,
    headers=updated_headers,
    json=payload_for_tool_call,
    stream=True,
)
print("Call Tool Response:")
print(response_tool_call.text)
