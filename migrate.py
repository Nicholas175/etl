# migrate.py
"""
Schiebt Daten aus der Staging-Tabelle ins Data-Warehouse-Schema
(dim_person / fact_activity).
"""
import pandas as pd
from sqlalchemy import text
from load import _get_engine


def stage_to_warehouse(staging_table: str = "staging_test") -> None:
    engine = _get_engine()

    with engine.begin() as conn:
        # ----------  1) DDL (idempotent) ----------
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dim_person (
              person_id  INT AUTO_INCREMENT PRIMARY KEY,
              name       VARCHAR(255) UNIQUE
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fact_activity (
              activity_id     INT AUTO_INCREMENT PRIMARY KEY,
              src_id          INT,
              person_id       INT,
              description     TEXT,
              age             INT,
              country         VARCHAR(100),
              activity_date   DATE,
              FOREIGN KEY (person_id) REFERENCES dim_person(person_id)
            )
        """))

        # ----------  2) Daten aus Staging holen ----------
        df = pd.read_sql(
            f"""
            SELECT
              src_id,
              TRIM(name)        AS name,
              TRIM(description) AS description,
              age,
              TRIM(country)     AS country,
              activity_date
            FROM {staging_table}
            """,
            conn,
        )
        if df.empty:
            print("Staging leer – nichts zu laden.")
            return

        # ----------  3) Dimension laden ----------
        df[["name"]].drop_duplicates().to_sql(
            "dim_person_tmp", conn, if_exists="replace", index=False
        )
        conn.execute(text("""
            INSERT IGNORE INTO dim_person (name)
            SELECT name FROM dim_person_tmp
        """))
        conn.execute(text("DROP TABLE dim_person_tmp"))

        # ----------  4) Person-IDs auflösen & Fakt laden ----------
        person_map = pd.read_sql(
            "SELECT person_id, name FROM dim_person", conn
        )

        fact_df = (
            df.merge(person_map, on="name", how="inner")
              [["src_id", "person_id", "description", "age",
                "country", "activity_date"]]
        )
        fact_df.to_sql(
            "fact_activity", conn, if_exists="append", index=False
        )

        print(f"Loaded {len(fact_df)} rows into 'fact_activity' (append).")


if __name__ == "__main__":
    stage_to_warehouse()
