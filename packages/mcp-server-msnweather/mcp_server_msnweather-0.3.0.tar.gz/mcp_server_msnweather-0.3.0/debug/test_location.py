import asyncio
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server_msnweather.server import initialize_mcp, get_location_coordinates

async def main():
    # Get API keys from environment variables
    weather_api_key = os.getenv('MSN_WEATHER_API_KEY')
    autosuggest_apikey = os.getenv('BING_MAPS_API_KEY')
    
    if not weather_api_key:
        print("Error: MSN_WEATHER_API_KEY environment variable not set")
        sys.exit(1)
        
    if not autosuggest_apikey:
        print("Error: BING_MAPS_API_KEY environment variable not set")
        sys.exit(1)
        
    # Initialize with both API keys
    initialize_mcp(weather_api_key, autosuggest_apikey)
    
    # Test locations
    test_locations = [
        "Seattle, WA",
        "New York, NY",
        "San Francisco, CA",
        "Tokyo, Japan",
        "London, UK"
    ]
    
    # Test with multiple locations
    for location in test_locations:
        try:
            print(f"\nLooking up coordinates for: {location}")
            locationInfo = await get_location_coordinates(location)
            
            if locationInfo:
                print(f"locationInfo: {locationInfo}")
            else:
                print(f"No coordinates found for {location}")
        except Exception as e:
            print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())