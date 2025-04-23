import asyncio
import os
import requests
from typing import Dict, Any

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}

# Environment validator for Workday API

class EnvValidator:
    def get_access_token(self) -> str:
        # Fetch access token from environment variable
        token = os.environ.get("WORKDAY_ACCESS_TOKEN")
        if not token:
            raise ValueError("WORKDAY_ACCESS_TOKEN environment variable is not set")
        return token

env_validator = EnvValidator()

server = Server("workday-mcp-new")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{name}"),
            name=f"Note: {name}",
            description=f"A simple note named {name}",
            mimeType="text/plain",
        )
        for name in notes
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific note's content by its URI.
    The note name is extracted from the URI host component.
    """
    if uri.scheme != "note":
        raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        return notes[name]
    raise ValueError(f"Note not found: {name}")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="Creates a summary of all notes",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="Style of the summary (brief/detailed)",
                    required=False,
                )
            ],
        )
    ]

@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    The prompt includes all current notes and can be customized via arguments.
    """
    if name != "summarize-notes":
        raise ValueError(f"Unknown prompt: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " Give extensive details." if style == "detailed" else ""

    return types.GetPromptResult(
        description="Summarize the current notes",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Here are the current notes to summarize:{detail_prompt}\n\n"
                    + "\n".join(
                        f"- {name}: {content}"
                        for name, content in notes.items()
                    ),
                ),
            )
        ],
    )

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="add-note",
            description="Add a new note",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="get-workday-workers",
            description="Fetch workers from Workday API",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        types.Tool(
            name="get-worker-eligible-absence-types",
            description="Fetch eligible absence types for a specific worker",
            inputSchema={
                "type": "object",
                "properties": {
                    "worker_id": {"type": "string"},
                },
                "required": ["worker_id"],
            },
        ),
        types.Tool(
            name="request-time-off",
            description="Submit a time off request for a worker",
            inputSchema={
                "type": "object",
                "properties": {
                    "worker_id": {"type": "string"},
                    "date": {"type": "string"},
                    "daily_quantity": {"type": "string"},
                    "time_off_type_id": {"type": "string"},
                },
                "required": ["worker_id", "date", "daily_quantity", "time_off_type_id"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can modify server state and notify clients of changes.
    """
    if name == "add-note":
        if not arguments:
            raise ValueError("Missing arguments")

        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("Missing name or content")

        # Update server state
        notes[note_name] = content

        # Notify clients that resources have changed
        await server.request_context.session.send_resource_list_changed()

        return [
            types.TextContent(
                type="text",
                text=f"Added note '{note_name}' with content: {content}",
            )
        ]
    elif name == "get-workday-workers":
        try:
            # Get validated access token from environment
            access_token = env_validator.get_access_token()
            
            url = "https://wd2-impl-services1.workday.com/ccx/api/staffing/v6/ibmsrv_pt1/workers/"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Successfully fetched workers from Workday API: {result}"
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error fetching workers from Workday API: {str(e)}"
                )
            ]
    elif name == "get-worker-eligible-absence-types":
        if not arguments:
            raise ValueError("Missing arguments")
            
        worker_id = arguments.get("worker_id")
        if not worker_id:
            raise ValueError("Missing worker_id argument")
            
        try:
            # Get validated access token from environment
            access_token = env_validator.get_access_token()
            
            base_url = "https://wd2-impl-services1.workday.com/ccx/api/absenceManagement/v2/ibmsrv_pt1"
            url = f"{base_url}/workers/{worker_id}/eligibleAbsenceTypes"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            params = {
                "limit": 100
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            result = response.json()
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Successfully fetched eligible absence types for worker {worker_id}: {result}"
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error fetching eligible absence types for worker {worker_id}: {str(e)}"
                )
            ]
    elif name == "request-time-off":
        if not arguments:
            raise ValueError("Missing arguments")
            
        worker_id = arguments.get("worker_id")
        date = arguments.get("date")
        daily_quantity = arguments.get("daily_quantity")
        time_off_type_id = arguments.get("time_off_type_id")
        
        if not all([worker_id, date, daily_quantity, time_off_type_id]):
            raise ValueError("Missing required arguments for time off request")
            
        try:
            # Get validated access token from environment
            access_token = env_validator.get_access_token()
            
            base_url = "https://wd2-impl-services1.workday.com/ccx/api/absenceManagement/v2/ibmsrv_pt1"
            url = f"{base_url}/workers/{worker_id}/requestTimeOff"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "days": [
                    {
                        "date": date,
                        "dailyQuantity": daily_quantity,
                        "timeOffType": {
                            "id": time_off_type_id
                        }
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            return [
                types.TextContent(
                    type="text",
                    text=f"Successfully requested time off for worker {worker_id}: {result}"
                )
            ]
        except Exception as e:
            return [
                types.TextContent(
                    type="text",
                    text=f"Error requesting time off for worker {worker_id}: {str(e)}"
                )
            ]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="workday-mcp-new",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )