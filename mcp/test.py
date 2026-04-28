import requests

def get_forecast_sync(latitude: float, longitude: float) -> str:
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"

    headers = {
        "User-Agent": "weather-app/1.0",
        "Accept": "application/geo+json"
    }

    # bước 1: lấy forecast URL
    res = requests.get(points_url, headers=headers, timeout=30)
    res.raise_for_status()
    points_data = res.json()

    forecast_url = points_data["properties"]["forecast"]

    # bước 2: lấy forecast data
    res2 = requests.get(forecast_url, headers=headers, timeout=30)
    res2.raise_for_status()
    forecast_data = res2.json()

    periods = forecast_data["properties"]["periods"]

    forecasts = []
    for p in periods[:5]:
        forecasts.append(
            f"{p['name']}: {p['temperature']}°{p['temperatureUnit']} - {p['detailedForecast']}"
        )

    return "\n".join(forecasts)

if __name__ == "__main__":
    lat = 37.7749
    lon = -122.4194
    print(get_forecast_sync(lat, lon))