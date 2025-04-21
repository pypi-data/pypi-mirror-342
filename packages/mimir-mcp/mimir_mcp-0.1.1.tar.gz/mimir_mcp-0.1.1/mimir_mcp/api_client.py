import os
import json
import httpx
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ApiConfig(BaseModel):
    base_url: str
    auth_token: str


class ApiClient:

    def __init__(self, config: ApiConfig):
        self.base_url = config.base_url
        self.auth_token = config.auth_token
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }

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


def load_config() -> ApiConfig:
    # try loading from environment variables first
    base_url = os.environ.get("MIMIR_API_URL")
    auth_token = os.environ.get("MIMIR_API_TOKEN")

    # if not found in environment, try loading from config file
    if not base_url or not auth_token:
        config_path = os.path.join(
            os.path.expanduser("~"), ".mimir", "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config_data = json.load(f)
                    base_url = base_url or config_data.get("api_url")
                    auth_token = auth_token or config_data.get("api_token")
            except (json.JSONDecodeError, FileNotFoundError):
                pass

    if not base_url:
        # default fallback
        base_url = "https://dev.trymimir.ai/api"

    if not auth_token:
        print("Warning: No API token found. Some API calls may fail.")
        auth_token = ""

    return ApiConfig(base_url=base_url, auth_token=auth_token)
