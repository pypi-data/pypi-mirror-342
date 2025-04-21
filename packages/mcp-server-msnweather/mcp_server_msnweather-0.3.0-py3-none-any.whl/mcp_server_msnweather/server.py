import sys
from typing import Any, Dict, Tuple, Optional
import httpx
from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
ALERTS_API_URL = "https://api.msn.com/weather/alerts?locale=en-us&lat={lat}&lon={lon}&apikey={apikey}"
FORECAST_API_URL = "https://api.msn.com/weather/dailyforecast?market=en-us&lat={lat}&lon={lon}&days=7&apikey={apikey}"
LOCATION_API_URL = "https://www.bing.com/api/v6/Places/AutoSuggest?appid={autosuggest_apikey}&count=1&q={query}&setmkt=en-us&setlang=en-us&types=Place,Address,Business&abbrtext=1&structuredaddress=true&strucaddrread=1"
sys.stdout.reconfigure(encoding='utf-8')
# Update mcp initialization to accept apikeys
def initialize_mcp(weather_apikey: str, autosuggest_apikey: str):
    """Initialize the MCP server with the provided API keys.
    
    Args:
        weather_apikey: API key for MSN weather services
        autosuggest_apikey: API key for Bing Maps services
    """
    global ALERTS_API_URL, FORECAST_API_URL, LOCATION_API_URL
    ALERTS_API_URL = ALERTS_API_URL.replace("{apikey}", weather_apikey)
    FORECAST_API_URL = FORECAST_API_URL.replace("{apikey}", weather_apikey)
    LOCATION_API_URL = LOCATION_API_URL.replace("{autosuggest_apikey}", autosuggest_apikey)

async def make_api_request(url: str) -> Any | None:
    """Make a request to an API with proper error handling."""
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

def parse_autosuggestion_result(suggestion_data: Dict) -> Optional[Dict]:
    """Parse the suggestion result from Bing Places API to extract coordinates and address.
    
    Args:
        suggestion_data: The suggestion data from Bing Places API
        
    Returns:
        A dictionary containing lat, lon, and address if successful, None otherwise
    """
    try:
        # Extract geo data from the input
        geo = suggestion_data.get("geo")
        if not geo or "latitude" not in geo or "longitude" not in geo:
            print("Missing or invalid geo data in suggestion result")
            return None
            
        # Extract lat and lon
        lat = geo["latitude"]
        lon = geo["longitude"]
        
        # Extract address data (set to empty dict if not present)
        address = suggestion_data.get("address", {})
        
        # Create the result dictionary
        result = {
            "lat": lat,
            "lon": lon,
            "address": address
        }
        
        return result
    except Exception as e:
        print(f"Error parsing autosuggestion result: {str(e)}")
        return None

async def location_to_coordinates(location_name: str) -> Optional[Dict]:
    """Convert a location name to latitude and longitude coordinates using Bing Places API.
    
    Args:
        location_name: Name of the location to look up
        
    Returns:
        A tuple of (latitude, longitude) if successful, None otherwise
    """
    if not location_name:
        print("Error: Empty location name provided")
        return None
        
    url = LOCATION_API_URL.format(query=location_name)
    data = await make_api_request(url)
    if not data:
        print(f"Unable to get coordinates for location: {location_name}")
        return None
    
    try:
        # Extract coordinates using the parsing function
        locations = data.get("value", [])
        if not locations:
            print(f"No location suggestions found for: {location_name}")
            return None
            
        # Get the first suggestion (most relevant)
        location = locations[0]
        location_data = parse_autosuggestion_result(location)
        
        if not location_data:
            return None
            
        # Extract lat and lon for backward compatibility
        return location_data
    except Exception as e:
        print(f"Error processing location data: {str(e)}")
        return None

@mcp.tool()
async def get_alerts(location_name: str) -> str:
    """Get weather alerts for a location by name.

    Args:
        location_name: Name of the location (e.g., "Seattle, WA")
    """
    # Convert location name to coordinates
    location_data = await location_to_coordinates(location_name)
    if not location_data:
        return f"Unable to find coordinates for location: {location_name}"
    
    # Extract latitude and longitude
    latitude = location_data["lat"]
    longitude = location_data["lon"]
    
    # Get alerts using the coordinates
    url = ALERTS_API_URL.format(lat=latitude, lon=longitude)
    data = await make_api_request(url)

    if not data:
        return "Unable to fetch alerts or no alerts found."

    return encode_json_utf8(data)

@mcp.tool()
async def get_forecast(location_name: str) -> str:
    """Get weather forecast for a location by name.

    Args:
        location_name: Name of the location (e.g., "Seattle, WA")
    """
    # Convert location name to coordinates
    location_data = await location_to_coordinates(location_name)
    if not location_data:
        return f"Unable to find coordinates for location: {location_name}"
    
    # Extract latitude and longitude
    latitude = location_data["lat"]
    longitude = location_data["lon"]
    
    # Get forecast using the coordinates
    url = FORECAST_API_URL.format(lat=latitude, lon=longitude)
    points_data = await make_api_request(url)
    if not points_data:
        return "Unable to fetch forecast data for this location."
    
    return encode_json_utf8(points_data)

@mcp.tool()
async def get_location_coordinates(location_name: str) -> str:
    """Convert a location name to complete location information including latitude and longitude coordinates, region,country, and address.

    Args:
        location_name: Name of the location to look up (e.g., "Seattle, WA")
    """
    result = await location_to_coordinates(location_name)
    
    if not result:
        return f"Unable to find coordinates for location: {location_name}"
        
    return encode_json_utf8(result)
