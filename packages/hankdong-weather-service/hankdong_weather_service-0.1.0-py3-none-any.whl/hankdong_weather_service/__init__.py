"""
Weather Service - A Python package for accessing weather data from NWS API
"""

__version__ = "0.1.0"

from .weather import get_alerts, get_forecast, mcp

__all__ = ["get_alerts", "get_forecast", "mcp"] 