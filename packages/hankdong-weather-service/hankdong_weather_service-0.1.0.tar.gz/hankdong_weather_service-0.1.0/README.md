# Hankdong Weather Service

A Python package for accessing weather data from the National Weather Service (NWS) API.

## Installation

```bash
pip install hankdong-weather-service
```

## Usage

```python
from hankdong_weather_service import get_alerts, get_forecast

# Get weather alerts for a state
alerts = await get_alerts("CA")  # California

# Get weather forecast for a location
forecast = await get_forecast(37.7749, -122.4194)  # San Francisco coordinates
```

## Features

- Get weather alerts for any US state
- Get detailed weather forecasts for any location
- Built on top of the NWS API
- Asynchronous API for better performance

## Requirements

- Python 3.8+
- httpx
- mcp-server

## License

MIT License 