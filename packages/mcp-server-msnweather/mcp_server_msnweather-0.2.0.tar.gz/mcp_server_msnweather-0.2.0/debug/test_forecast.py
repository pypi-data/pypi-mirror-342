import asyncio
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server_msnweather.server import initialize_mcp, get_forecast

async def main():
    # Get API key from environment variable
    api_key = os.getenv('MSN_WEATHER_API_KEY')
    if not api_key:
        print("Error: MSN_WEATHER_API_KEY environment variable not set")
        sys.exit(1)
        
    # Initialize with API key
    initialize_mcp(api_key)
    
    # Using Seattle coordinates (same as in tests)
    try:
        print(f"\nFetching forecast at {datetime.now()}")
        result = await get_forecast(47.6062, -122.3321)
        print(result)
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())