import unittest
from unittest.mock import AsyncMock, patch
from mcp_server_msnweather.server import initialize_mcp, get_alerts, get_forecast

class TestMcpServerMsnWeather(unittest.TestCase):
    def test_initialize_mcp(self):
        # Test if initialize_mcp correctly replaces API key in URLs
        initialize_mcp("test_api_key")
        self.assertIn("test_api_key", get_alerts.__globals__["ALERTS_API_URL"])
        self.assertIn("test_api_key", get_forecast.__globals__["FORECAST_API_URL"])

    @patch("mcp_server_msnweather.server.make_nws_request", new_callable=AsyncMock)
    async def test_get_alerts(self, mock_request):
        # Mock the response of make_nws_request
        mock_request.return_value = {"alerts": "Test Alert"}
        result = await get_alerts(47.6062, -122.3321)
        self.assertIn("Test Alert", result)

    @patch("mcp_server_msnweather.server.make_nws_request", new_callable=AsyncMock)
    async def test_get_forecast(self, mock_request):
        # Mock the response of make_nws_request
        mock_request.return_value = {"forecast": "Test Forecast"}
        result = await get_forecast(47.6062, -122.3321)
        self.assertIn("Test Forecast", result)

if __name__ == "__main__":
    unittest.main()