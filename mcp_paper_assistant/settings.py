import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Literal, Dict

from dotenv import load_dotenv

load_dotenv()


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MCP_", case_sensitive=False)

    name: str = "mcp-paper-assistant"
    host: str = "127.0.0.1"
    transport: Literal["http", "stdio", "streamable-http"] = "http"
    port: int = 3031
    path: Optional[str] = None
    log_level: str = "info"


class ArxivSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ARXIV_", case_sensitive=False
    )

    max_results: int = 10


class ModelSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MODEL_", case_sensitive=False
    )

    model: str
    temperature: float = 0.2
