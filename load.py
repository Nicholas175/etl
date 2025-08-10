# load.py
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db import _get_engine


# ----------  Laden in Staging  ----------
def load_to_staging_weather(
    df: pd.DataFrame,
    table: str = "staging_weather",
    if_exists: str = "replace",
    chunksize: int = 1_000,
) -> None:
    """
    Legt die Staging-Tabelle für Wetterdaten neu an (DROP + CREATE) und lädt die Daten hinein.
    """
    engine: Engine = _get_engine()

    with engine.begin() as conn:
        # Tabelle komplett neu anlegen
        conn.execute(text("DROP TABLE IF EXISTS staging_weather"))
        conn.execute(text("""
            CREATE TABLE staging_weather (
              record_id      INT,
              temp           FLOAT,
              rain_mm        FLOAT,
              wind_speed     FLOAT,
              datum          DATE,
              uhrzeit        TIME,
              stadt          VARCHAR(255),
              breitengrad    FLOAT,
              laengengrad    FLOAT,
              datenquelle    VARCHAR(255),
              PRIMARY KEY (record_id)
            )
        """))

    # DataFrame in MySQL schreiben
    df.to_sql(table, con=engine, if_exists="append", index=False, chunksize=chunksize)
    print(f"✅ Loaded {len(df)} rows into '{table}'.")


if __name__ == "__main__":
    from extract import extract_raw
    from transform import transform

    raw_df   = extract_raw()
    clean_df = transform(raw_df)
    load_to_staging_weather(clean_df)
