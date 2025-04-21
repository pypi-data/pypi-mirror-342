# File: trianglengin/__init__.py
"""
Triangle Engine Library (`trianglengin`)

Core components for a triangle puzzle game environment.
"""

# Expose key components from submodules
from . import app, cli, config, core, interaction, visualization

__all__ = [
    "core",
    "config",
    "visualization",
    "interaction",
    "app",
    "cli",
]
