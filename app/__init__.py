"""App factory: builds and configures the Flask app.

Gunicorn (on Render) and run.py (locally) both call create_app().
All settings come from environment variables, never hardcoded.
"""
import os

from dotenv import load_dotenv
from flask import Flask


def create_app(config_overrides=None):
    # Load .env for local development. On Render, real env vars are used.
    load_dotenv()

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-not-secret"),
        DATABASE_URL=os.environ.get("DATABASE_URL", ""),
        ANTHROPIC_API_KEY=os.environ.get("ANTHROPIC_API_KEY", ""),
        ANTHROPIC_MODEL=os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
    )

    # Tests pass overrides here instead of touching real env vars.
    if config_overrides:
        app.config.update(config_overrides)

    from app.routes import bp

    app.register_blueprint(bp)
    return app
