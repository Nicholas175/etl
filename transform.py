# transform.py
import pandas as pd

def transform_weather_data(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    """
    Transformiert den DataFrame:
    - Splittet die Spalte 'time' in 'date' und 'hour'
    - Entfernt 'time'
    - Fügt eine ID-Spalte hinzu
    - Fügt Meta-Infos (Übergabeparameter) an jede Zeile an
    - Bennent alle Spalten anhand eines Mappings um
    """

    # 1) time in datetime konvertieren
    df["time"] = pd.to_datetime(df["time"], errors="coerce")

    # 2) neue Spalten für Datum und Uhrzeit
    df["date"] = df["time"].dt.date
    df["hour"] = df["time"].dt.time

    # 3) 'time' entfernen, da wir date & hour haben
    df = df.drop(columns=["time"])

    # 4) ID-Spalte erstellen (laufend ab 1)
    df.insert(0, "ID", range(1, len(df) + 1))

    # 5) Meta-Infos anfügen (z. B. Stadt, Koordinaten)
    for key, value in meta.items():
        df[key] = value

    # 6) Spalten-Mapping definieren (Zielnamen beliebig anpassbar)
    spalten_mapping = {
        "ID": "record_id",
        "temperature_2m": "temp",
        "precipitation": "rain_mm",
        "windspeed_10m": "wind_speed",
        "date": "datum",
        "hour": "uhrzeit",
        "city": "stadt",
        "lat": "breitengrad",
        "lon": "laengengrad",
        "source": "datenquelle"
    }

    # 7) Spalten umbenennen
    df = df.rename(columns=spalten_mapping)

    return df



if __name__ == "__main__":
    # Dummy-Test (wird nur ausgeführt, wenn man die Datei direkt startet)
    test_data = {
        "time": ["2025-07-01 00:00:00", "2025-07-01 01:00:00"],
        "temperature_2m": [20.1, 19.8],
        "precipitation": [0.0, 0.1],
        "windspeed_10m": [3.5, 3.0]
    }
    df_test = pd.DataFrame(test_data)

    meta_info = {
        "city": "Gütersloh",
        "lat": 51.9,
        "lon": 8.4,
        "source": "open-meteo"
    }

    df_transformed = transform_weather_data(df_test, meta_info)
    print("Transformierter DF:\n", df_transformed)
