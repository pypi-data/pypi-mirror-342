# MCP Server MSN Weather

A Model Context Protocol (MCP) server that provides weather data using the MSN Weather API. This server enables access to weather alerts and forecasts for any location using latitude and longitude coordinates.

## Installation

```bash
pip install mcp-server-msnweather
```

## Requirements

- Python >= 3.10
- httpx >= 0.28.1
- mcp[cli] >= 1.2.0

## Usage

1. First, obtain an MSN Weather API key from Microsoft.

2. Start the server with your API key:

```bash
mcp-server-msnweather --apikey YOUR_API_KEY
```

## Available Tools

### get_alerts

Fetches weather alerts for a specific location.

Parameters:
- `latitude` (float): Latitude of the location
- `longitude` (float): Longitude of the location

Example:
```python
result = await mcp.call_tool("get_alerts", {
    "latitude": 47.6062,
    "longitude": -122.3321
})
```

### get_forecast

Gets a 7-day weather forecast for a specific location.

Parameters:
- `latitude` (float): Latitude of the location
- `longitude` (float): Longitude of the location

Example:
```python
result = await mcp.call_tool("get_forecast", {
    "latitude": 47.6062,
    "longitude": -122.3321
})
```

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-server-msnweather.git
cd mcp-server-msnweather

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## License

See the [LICENSE](LICENSE) file for details.
