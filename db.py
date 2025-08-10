"""Database connection utilities."""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()


def _get_engine() -> Engine:
    user = os.getenv("DB_USER", "etl_user")
    password = os.getenv("DB_PASSWORD", "EtLpw123")
    host = os.getenv("DB_HOST", "mariadb")
    port = os.getenv("DB_PORT", "3306")
    database = os.getenv("DB_NAME", "etl_db")

    # Für TCP-Verbindung localhost → 127.0.0.1 erzwingen
    if host == "localhost":
        host = "127.0.0.1"

    return create_engine(
        f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    )
