import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server_msnweather.server import initialize_mcp, get_alerts

async def main():
    # Get API key from environment variable
    api_key = os.getenv('MSN_WEATHER_API_KEY')
    if not api_key:
        print("Error: MSN_WEATHER_API_KEY environment variable not set")
        sys.exit(1)
        
    # Initialize with API key
    initialize_mcp(api_key)
    
    # Using Seattle coordinates (same as in tests)
    result = await get_alerts(33.596318961132695, 130.40771484375)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())