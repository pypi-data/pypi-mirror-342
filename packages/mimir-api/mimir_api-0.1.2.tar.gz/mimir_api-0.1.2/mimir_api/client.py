import os
import json
import httpx
from typing import Any, Dict, Optional
from pydantic import BaseModel


class MimirConfig(BaseModel):
    base_url: str
    api_key: str


class MimirClient:
    """Main API client for Mimir API."""

    def __init__(self, config: MimirConfig):
        self.base_url = config.base_url
        self.api_key = config.api_key
        self.headers = {
            "X-API-Key": config.api_key,
            "Content-Type": "application/json"
        }
        
        from .repositories import RepositoriesAPI
        self.repositories = RepositoriesAPI(self)

        from .tools import ToolsAPI
        self.tools = ToolsAPI(self)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=self.headers,
                timeout=30.0
            )

            response.raise_for_status()
            if response.status_code == 204:  # no content
                return None

            return response.json()


def load_config() -> MimirConfig:
    # try loading from environment variables first
    base_url = os.environ.get("MIMIR_API_URL")
    api_key = os.environ.get("MIMIR_API_KEY")

    # if not found in environment, try loading from config file
    if not base_url or not api_key:
        config_path = os.path.join(
            os.path.expanduser("~"), ".mimir", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config_data = json.load(f)
                    base_url = base_url or config_data.get("api_url")
                    api_key = api_key or config_data.get("api_key")
            except (json.JSONDecodeError, FileNotFoundError):
                pass

    if not base_url:
        # default fallback
        base_url = "https://dev.trymimir.ai/api"

    if not api_key:
        print("Warning: No API key found. API calls will fail.")
        api_key = ""

    return MimirConfig(base_url=base_url, api_key=api_key)