import sys
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
ALERTS_API_URL = "https://api.msn.com/weather/alerts?locale=en-us&lat={lat}&lon={lon}&apikey={apikey}"
FORECAST_API_URL = "https://api.msn.com/weather/dailyforecast?market=en-us&lat={lat}&lon={lon}&days=7&apikey={apikey}"
sys.stdout.reconfigure(encoding='utf-8')
# Update mcp initialization to accept apikey
def initialize_mcp(apikey: str):
    """Initialize the MCP server with the provided API key."""
    global ALERTS_API_URL, FORECAST_API_URL
    ALERTS_API_URL = ALERTS_API_URL.replace("{apikey}", apikey)
    FORECAST_API_URL = FORECAST_API_URL.replace("{apikey}", apikey)

async def make_api_request(url: str) -> Any | None:
    """Make a request to the NWS API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error in make_api_request: {str(e)}")
            return None

def encode_json_utf8(data: Any) -> str:
    """Encode data as JSON with UTF-8."""
    try:
        # First convert to JSON string
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        print(f"Error encoding to UTF-8: {str(e)}")
        return "Error encoding response data"

@mcp.tool()
async def get_alerts(latitude: float, longitude: float) -> str:
    """Get weather alerts for a US state.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = ALERTS_API_URL.format(lat=latitude, lon=longitude)
    data = await make_api_request(url)

    if not data:
        return "Unable to fetch alerts or no alerts found."

    return encode_json_utf8(data)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    url = FORECAST_API_URL.format(lat=latitude, lon=longitude)
    points_data = await make_api_request(url)
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    return encode_json_utf8(points_data)
