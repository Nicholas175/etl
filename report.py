# report.py
from typing import Any
import pandas as pd
from sqlalchemy import create_engine, text


# ----------  Report-SQL  ----------
_SQL_REPORT = text("""
    SELECT
      f.src_id,
      d.name,
      f.description,
      f.age,
      f.country,
      f.activity_date
    FROM fact_activity AS f
    JOIN dim_person    AS d ON f.person_id = d.person_id
    ORDER BY f.src_id
""")


# ----------  DB-Verbindung  ----------
def _get_engine() -> Any:
    user     = "etl_user"
    password = "EtLpw123"
    host     = "mariadb"
    port     = "3306"
    database = "etl_db"

    if host == "localhost":
        host = "127.0.0.1"

    return create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    )


# ----------  Report abrufen  ----------
def fetch_report() -> pd.DataFrame:
    """Liefert den vollständigen Report als DataFrame."""
    engine = _get_engine()
    with engine.connect() as conn:
        return pd.read_sql(_SQL_REPORT, conn)


if __name__ == "__main__":
    print(fetch_report())
