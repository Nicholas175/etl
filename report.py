# report.py
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db import _get_engine


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


# ----------  Report abrufen  ----------
def fetch_report() -> pd.DataFrame:
    """Liefert den vollständigen Report als DataFrame."""
    engine: Engine = _get_engine()
    with engine.connect() as conn:
        return pd.read_sql(_SQL_REPORT, conn)


if __name__ == "__main__":
    print(fetch_report())
