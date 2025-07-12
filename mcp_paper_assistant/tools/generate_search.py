from openai import AsyncOpenAI
import os
import json
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

from fastmcp.tools.tool import ToolResult
from fastmcp.exceptions import ToolError

from dotenv import load_dotenv

from mcp_paper_assistant.settings import ModelSettings
load_dotenv()

# Load prompt from JSON file
def load_prompt(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["system_prompt"]

PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts"/ "system_prompt.json"
assert PROMPT_PATH, f"Path {PROMPT_PATH} does not exist"
system_prompt = load_prompt(PROMPT_PATH)
model_settings = ModelSettings()

async def extract_search_arguments(user_query: str) -> Dict[str, Optional[str]]:
    client = AsyncOpenAI()
    MODEL = model_settings.model
    TEMPERATURE = model_settings.temperature

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    try:

        response = await client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            functions=[
                {
                    "name": "generate_search_args",
                    "description": "Extracts structured search parameters from user input",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Main topic of the papers"},
                            "max_results": {"type": ["integer", "null"], "description": "Max number of papers to return"},
                            "date_from": {"type": ["string", "null"], "format": "date", "description": "Start date"},
                            "date_to": {"type": ["string", "null"], "format": "date", "description": "End date"},
                        },
                        "required": ["query", "max_results", "date_from", "date_to"]
                    },
                }
            ],
            function_call={"name": "generate_search_args"},
        )

        function_args = response.choices[0]["message"]["function_call"]["arguments"]
        parsed_args = json.loads(function_args)

        return ToolResult(structured_content=parsed_args)
    except Exception as e:
        return ToolError(e)
