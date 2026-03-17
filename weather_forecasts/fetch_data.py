#!/usr/bin/env python3
"""
Download current weather and 5-day forecasts from OpenWeatherMap API 2.5
for all cities listed in list.txt.

Usage:
    python fetch_data.py --api-key YOUR_API_KEY
    # or set the OPENWEATHER_API_KEY environment variable and run:
    python fetch_data.py
"""

import argparse
import json
import os
import time
from pathlib import Path

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5"
CURRENT_WEATHER_URL = f"{BASE_URL}/weather"
FORECAST_URL = f"{BASE_URL}/forecast"

SCRIPT_DIR = Path(__file__).parent
LIST_FILE = SCRIPT_DIR / "list.txt"
DATA_DIR = SCRIPT_DIR / "data"
CURRENT_WEATHER_DIR = DATA_DIR / "current_weather"
FORECAST_DIR = DATA_DIR / "forecast"

# Delay between API calls to avoid hitting rate limits (seconds)
REQUEST_DELAY = 0.5


def load_cities(list_file: Path) -> list[str]:
    """Load city names from the list file, skipping blank lines."""
    cities = []
    with open(list_file, encoding="utf-8") as f:
        for line in f:
            city = line.strip()
            if city:
                cities.append(city)
    return cities


def fetch_weather(url: str, city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch weather data from the given endpoint for a city."""
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, path: Path) -> None:
    """Save a dictionary as a pretty-printed JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch current weather and 5-day forecasts from OpenWeatherMap API 2.5."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("OPENWEATHER_API_KEY"),
        help="OpenWeatherMap API key (or set OPENWEATHER_API_KEY env variable).",
    )
    parser.add_argument(
        "--units",
        default="metric",
        choices=["metric", "imperial", "standard"],
        help="Units of measurement (default: metric).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=REQUEST_DELAY,
        help=f"Delay in seconds between API calls (default: {REQUEST_DELAY}).",
    )
    args = parser.parse_args()

    if not args.api_key:
        parser.error(
            "API key is required. Pass --api-key or set the OPENWEATHER_API_KEY environment variable."
        )

    cities = load_cities(LIST_FILE)
    print(f"Loaded {len(cities)} cities from {LIST_FILE}")

    success_count = 0
    error_count = 0

    for i, city in enumerate(cities, start=1):
        print(f"[{i}/{len(cities)}] {city}", end=" ... ", flush=True)

        try:
            # --- Current weather ---
            current = fetch_weather(CURRENT_WEATHER_URL, city, args.api_key, args.units)
            save_json(current, CURRENT_WEATHER_DIR / f"{city}.json")
            time.sleep(args.delay)

            # --- 5-day / 3-hour forecast ---
            forecast = fetch_weather(FORECAST_URL, city, args.api_key, args.units)
            save_json(forecast, FORECAST_DIR / f"{city}.json")
            time.sleep(args.delay)

            print("OK")
            success_count += 1

        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
            error_count += 1
        except requests.RequestException as e:
            print(f"Request error: {e}")
            error_count += 1

    print(f"\nDone. {success_count} succeeded, {error_count} failed.")


if __name__ == "__main__":
    main()
