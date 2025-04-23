from datetime import date
from typing import Any

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from feedmob_mcp_adjust.internal_api_service import InternalApiService

mcp = FastMCP(name="Feedmob MCP Server of Adjust")


@mcp.tool()
def get_adjust_all_supported_clients() -> list[dict[str, Any]]:
    """Get all supported clients for loading Adjust reports."""
    return InternalApiService().get_all_supported_clients()


@mcp.tool()
def get_adjust_event_metrics_for_client(
    client: str = Field(..., description="Client name"),
) -> list[dict]:
    """Get event metrics for the client. Includes app_tokens and metrics"""
    return InternalApiService().get_event_metrics(client_name=client)


@mcp.tool()
def get_adjust_channels_params_for_client(
    client: str = Field(..., description="Client name"),
) -> list[str]:
    """Get report channels parameters for the client."""
    return InternalApiService().get_channels(client_name=client)


@mcp.tool()
def get_adjust_reports(
    client: str = Field(..., description="Client name"),
    start_date: date = Field(..., description="Start date for the report"),
    end_date: date = Field(..., description="End date for the report"),
    channels: list[str] = Field([], description="Channels for the report"),
    metrics: list[str] = Field([], description="Metrics for the report"),
    app_tokens: list[str] = Field([], description="App tokens for the report"),
) -> str:
    """Get Adjust reports for the client."""
    return InternalApiService().get_report(
        client_name=client,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        channels=channels,
        metrics=metrics,
        app_tokens=app_tokens,
    )


async def main():
    await mcp.run_stdio_async()
