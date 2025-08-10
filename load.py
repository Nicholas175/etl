# load.py
from typing import Any
import pandas as pd
from sqlalchemy import create_engine, text


# ----------  Verbindung  ----------
def _get_engine() -> Any:
    user     = "etl_user"
    password = "EtLpw123"
    host     = "mariadb"
    port     = "3306"
    database = "etl_db"

    # Für TCP-Verbindung localhost → 127.0.0.1 erzwingen
    if host == "localhost":
        host = "127.0.0.1"

    return create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    )


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
    engine = _get_engine()

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
