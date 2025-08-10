# extract.py

import requests
import pandas as pd

def extract_weather_data(lat: float, lon: float, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Lädt Wetterdaten von Open-Meteo für die angegebene Location und Zeitspanne.

    Args:
        lat (float): Breitengrad (Latitude)
        lon (float): Längengrad (Longitude)
        start_date (str): Startdatum im Format YYYY-MM-DD
        end_date (str): Enddatum im Format YYYY-MM-DD

    Returns:
        pd.DataFrame: DataFrame mit stündlichen Wetterdaten
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "precipitation", "windspeed_10m"],
        "timezone": "Europe/Berlin"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if "hourly" not in data:
        raise ValueError("Keine Wetterdaten in der API-Antwort gefunden.")

    df = pd.DataFrame(data["hourly"])
    return df

if __name__ == "__main__":
    # Testaufruf
    df_test = extract_weather_data(
        lat=51.9,
        lon=8.4,
        start_date="2025-07-01",
        end_date="2025-07-07"
    )
    print(df_test.head())
    print(f"{len(df_test)} Zeilen geladen.")
