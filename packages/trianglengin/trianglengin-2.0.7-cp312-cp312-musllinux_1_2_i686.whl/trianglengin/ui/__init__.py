# src/trianglengin/ui/__init__.py
"""
UI components for the Triangle Engine, including interactive modes
and visualization. Requires 'pygame' and 'typer'.
"""

# Directly import the components. Dependencies are now required.
from .app import Application
from .cli import app as cli_app
from .config import DEFAULT_DISPLAY_CONFIG, DisplayConfig
from .interaction import InputHandler
from .visualization import Visualizer

__all__ = [
    "Application",
    "cli_app",
    "DisplayConfig",
    "DEFAULT_DISPLAY_CONFIG",
    "InputHandler",
    "Visualizer",
]
