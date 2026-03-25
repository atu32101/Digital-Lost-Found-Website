import os
from dataclasses import dataclass


def _get_float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class Config:
    """
    App configuration loaded from environment variables.
    """

    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-please")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-please-too")

    # SQLAlchemy database URL (SQLite by default)
    # Use an absolute path so SQLite works regardless of current working directory.
    _default_sqlite_db_path: str = os.path.join(_BACKEND_DIR, "lost_found.db")
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_default_sqlite_db_path}")

    UPLOAD_FOLDER: str = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(_BACKEND_DIR, "uploads"),
    )
    MAX_CONTENT_LENGTH_MB: int = int(os.getenv("MAX_CONTENT_LENGTH_MB", "5"))

    # Example toggle: enable debug
    DEBUG: bool = FLASK_ENV != "production"


def get_config():
    """
    Returns a dict-like config for Flask's config loader.
    """
    c = Config()
    return {
        "ENV": c.FLASK_ENV,
        "SECRET_KEY": c.SECRET_KEY,
        "JWT_SECRET_KEY": c.JWT_SECRET_KEY,
        "SQLALCHEMY_DATABASE_URI": c.DATABASE_URL,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "UPLOAD_FOLDER": c.UPLOAD_FOLDER,
        "MAX_CONTENT_LENGTH": c.MAX_CONTENT_LENGTH_MB * 1024 * 1024,
        "DEBUG": c.DEBUG,
    }

