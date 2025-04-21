import asyncio
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server_msnweather.server import initialize_mcp, get_forecast

async def main():
    # Get API keys from environment variables
    weather_api_key = os.getenv('MSN_WEATHER_API_KEY')
    bing_api_key = os.getenv('BING_MAPS_API_KEY')
    
    if not weather_api_key:
        print("Error: MSN_WEATHER_API_KEY environment variable not set")
        sys.exit(1)
        
    if not bing_api_key:
        print("Error: BING_MAPS_API_KEY environment variable not set")
        sys.exit(1)
        
    # Initialize with API keys
    initialize_mcp(weather_api_key, bing_api_key)
    
    # Using location name instead of coordinates
    try:
        print(f"\nFetching forecast at {datetime.now()}")
        result = await get_forecast("Seattle, WA")
        print(result)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())