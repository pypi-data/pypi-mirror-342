# trianglengin/config/__init__.py
"""
Shared configuration models for the Triangle Engine.
"""

from .display_config import DEFAULT_DISPLAY_CONFIG, DisplayConfig
from .env_config import EnvConfig

__all__ = ["EnvConfig", "DisplayConfig", "DEFAULT_DISPLAY_CONFIG"]
