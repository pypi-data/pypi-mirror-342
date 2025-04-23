import os

import httpx
from httpx import Timeout


class InternalApiService:
    """
    Service for interacting with the MCP Internal API.
    """

    BASE_URL = "https://mcp-apis.feedmob.com/api/v1/adjust"

    def __init__(self):
        """Initialize with API credentials.

        Args:
            access_config: Dictionary containing API credentials
        """
        api_key = os.environ.get("INTERNAL_API_KEY")
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def get_all_supported_clients(self) -> list[dict]:
        response = httpx.get(
            f"{self.BASE_URL}/clients",
            headers=self.headers,
        )

        if response.is_error:
            raise httpx.HTTPStatusError(
                f"Error {response.status_code}: {response.text}",
                request=response.request,
                response=response,
            )

        return response.json().get("clients", "")

    def get_event_metrics(self, client_name: str) -> list[dict]:
        response = httpx.get(
            f"{self.BASE_URL}/clients/{client_name}/event_metrics",
            headers=self.headers,
        )
        if response.is_error:
            raise httpx.HTTPStatusError(
                f"Error {response.status_code}: {response.text}",
                request=response.request,
                response=response,
            )
        return response.json().get("event_metrics", [])

    def get_channels(self, client_name: str) -> list[str]:
        response = httpx.get(
            f"{self.BASE_URL}/clients/{client_name}/channels",
            headers=self.headers,
        )

        if response.is_error:
            raise httpx.HTTPStatusError(
                f"Error {response.status_code}: {response.text}",
                request=response.request,
                response=response,
            )

        return response.json().get("channels", [])

    def get_report(
        self,
        client_name: str,
        start_date: str,
        end_date: str,
        channels: list[str],
        metrics: list[str],
        app_tokens: list[str],
    ) -> str:
        request_params = {
            "client_name": client_name,
            "start_date": start_date,
            "end_date": end_date,
            "channels": ",".join(channels),
            "metrics": ",".join(metrics),
            "app_tokens": ",".join(app_tokens),
        }
        response = httpx.get(
            f"{self.BASE_URL}/reports",
            params=request_params,
            headers=self.headers,
            timeout=Timeout(120, connect=60, read=60, write=60),
        )
        if response.is_error:
            raise httpx.HTTPStatusError(
                f"Error {response.status_code}: {response.text}",
                request=response.request,
                response=response,
            )
        return response.content.decode("utf-8")
