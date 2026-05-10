# tools/search/get_weather_forecast.py

import requests
from tools.base import BaseTool


class GetWeatherForecastTool(BaseTool):
    name = "get_weather_forecast"
    description = "Get weather forecast by latitude and longitude"
    title = "Get Weather Forecast"

    async def execute(self, latitude: float, longitude: float):
        points_url = (
            f"https://api.weather.gov/points/{latitude},{longitude}"
        )

        headers = {
            "User-Agent": "weather-app/1.0",
            "Accept": "application/geo+json"
        }

        # Step 1: Get forecast URL
        res = requests.get(
            points_url,
            headers=headers,
            timeout=30
        )
        res.raise_for_status()

        points_data = res.json()
        forecast_url = points_data["properties"]["forecast"]

        # Step 2: Get forecast data
        res2 = requests.get(
            forecast_url,
            headers=headers,
            timeout=30
        )
        res2.raise_for_status()

        forecast_data = res2.json()
        periods = forecast_data["properties"]["periods"]

        forecasts = []

        for p in periods[:5]:
            forecasts.append(
                f"{p['name']}: "
                f"{p['temperature']}°{p['temperatureUnit']} - "
                f"{p['detailedForecast']}"
            )

        return "\n".join(forecasts)