"""Interfaces module for user interaction"""

from .cli.main import app as cli_app
from .web.fastapi_app import create_app

__all__ = ["cli_app", "create_app"]
