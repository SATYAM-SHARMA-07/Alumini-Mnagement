"""Application configuration module."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration for the Flask application."""

    SECRET_KEY = "change-this-secret-key-in-production"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'alumni.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
