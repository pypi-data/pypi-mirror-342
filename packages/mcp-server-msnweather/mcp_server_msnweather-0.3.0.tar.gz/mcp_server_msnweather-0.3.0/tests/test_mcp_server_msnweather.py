import unittest
from unittest.mock import AsyncMock, patch
from mcp_server_msnweather.server import initialize_mcp, get_alerts, get_forecast, location_to_coordinates

class TestMcpServerMsnWeather(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Initialize with test API keys before each test
        initialize_mcp("test_weather_api_key", "test_bing_api_key")

    def test_initialize_mcp(self):
        # Test if initialize_mcp in setUp correctly replaced API keys in URLs
        self.assertIn("test_weather_api_key", get_alerts.__globals__["ALERTS_API_URL"])
        self.assertIn("test_weather_api_key", get_forecast.__globals__["FORECAST_API_URL"])
        self.assertIn("test_bing_api_key", location_to_coordinates.__globals__["LOCATION_API_URL"])

    @patch("mcp_server_msnweather.server.location_to_coordinates", new_callable=AsyncMock)
    @patch("mcp_server_msnweather.server.make_api_request", new_callable=AsyncMock)
    async def test_get_alerts(self, mock_api_request, mock_location):
        # Mock the location_to_coordinates response
        mock_location.return_value = {
            "lat": 47.6062,
            "lon": -122.3321,
            "address": {"locality": "Seattle", "adminDistrict": "WA"}
        }
        
        # Mock the make_api_request response
        mock_api_request.return_value = {"alerts": "Test Alert"}
        
        # Call the function with a location name
        result = await get_alerts("Seattle, WA")
        
        # Verify location_to_coordinates was called with the correct argument
        mock_location.assert_called_once_with("Seattle, WA")
        
        # Verify make_api_request was called with the correct URL format
        # Extract the URL from the call args
        called_url = mock_api_request.call_args[0][0]
        self.assertIn("47.6062", called_url)  # latitude
        self.assertIn("-122.3321", called_url)  # longitude
        self.assertIn("test_weather_api_key", called_url)  # API key
        
        # Check that our mocked alert is in the result
        self.assertIn("Test Alert", result)

    @patch("mcp_server_msnweather.server.location_to_coordinates", new_callable=AsyncMock)
    @patch("mcp_server_msnweather.server.make_api_request", new_callable=AsyncMock)
    async def test_get_forecast(self, mock_api_request, mock_location):
        # Mock the location_to_coordinates response
        mock_location.return_value = {
            "lat": 47.6062,
            "lon": -122.3321,
            "address": {"locality": "Seattle", "adminDistrict": "WA"}
        }
        
        # Mock the make_api_request response
        mock_api_request.return_value = {"forecast": "Test Forecast"}
        
        # Call the function with a location name
        result = await get_forecast("Seattle, WA")
        
        # Verify location_to_coordinates was called with the correct argument
        mock_location.assert_called_once_with("Seattle, WA")
        
        # Verify make_api_request was called with the correct URL format
        # Extract the URL from the call args
        called_url = mock_api_request.call_args[0][0]
        self.assertIn("47.6062", called_url)  # latitude
        self.assertIn("-122.3321", called_url)  # longitude
        self.assertIn("test_weather_api_key", called_url)  # API key
        
        # Check that our mocked forecast is in the result
        self.assertIn("Test Forecast", result)

    @patch("mcp_server_msnweather.server.make_api_request", new_callable=AsyncMock)
    async def test_location_to_coordinates(self, mock_api_request):
        # Mock the API response
        mock_api_request.return_value = {
            "value": [{
                "geo": {
                    "latitude": 47.6062,
                    "longitude": -122.3321
                },
                "address": {
                    "locality": "Seattle",
                    "adminDistrict": "WA"
                }
            }]
        }
        
        # Call the function
        result = await location_to_coordinates("Seattle, WA")
        
        # Verify make_api_request was called with the correct URL format
        called_url = mock_api_request.call_args[0][0]
        self.assertIn("test_bing_api_key", called_url)  # API key
        self.assertIn("q=Seattle, WA", called_url)  # Location name (not URL encoded)
        
        # Verify result has expected fields
        self.assertEqual(result["lat"], 47.6062)
        self.assertEqual(result["lon"], -122.3321)
        self.assertIn("address", result)

if __name__ == "__main__":
    unittest.main()