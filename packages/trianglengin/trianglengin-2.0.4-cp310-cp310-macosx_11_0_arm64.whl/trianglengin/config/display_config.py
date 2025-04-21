# trianglengin/config/display_config.py
"""
Configuration specific to display and visualization settings.
"""

import pygame
from pydantic import BaseModel, Field

# Initialize Pygame font module if not already done (safe to call multiple times)
pygame.font.init()

# Define a placeholder font loading function or load directly here
# In a real app, this might load from files or use system fonts more robustly.
try:
    DEBUG_FONT_DEFAULT = pygame.font.SysFont("monospace", 12)
except Exception:
    DEBUG_FONT_DEFAULT = pygame.font.Font(None, 15)  # Fallback default pygame font


class DisplayConfig(BaseModel):
    """Configuration for visualization display settings."""

    # Screen and Layout
    SCREEN_WIDTH: int = Field(default=1024, gt=0)
    SCREEN_HEIGHT: int = Field(default=768, gt=0)
    FPS: int = Field(default=60, gt=0)
    PADDING: int = Field(default=10, ge=0)
    HUD_HEIGHT: int = Field(default=30, ge=0)
    PREVIEW_AREA_WIDTH: int = Field(default=150, ge=50)
    PREVIEW_PADDING: int = Field(default=5, ge=0)
    PREVIEW_INNER_PADDING: int = Field(default=3, ge=0)
    PREVIEW_BORDER_WIDTH: int = Field(default=1, ge=0)
    PREVIEW_SELECTED_BORDER_WIDTH: int = Field(default=3, ge=0)

    # Fonts (Store font objects directly or paths/names)
    # Using Field(default=...) requires the default value to be simple.
    # For complex objects like fonts, use default_factory or initialize in __init__.
    # For simplicity here, we'll assign the pre-loaded font.
    # Consider using default_factory=lambda: pygame.font.SysFont(...)
    DEBUG_FONT: pygame.font.Font = Field(default=DEBUG_FONT_DEFAULT)

    class Config:
        arbitrary_types_allowed = True  # Allow pygame.font.Font


# Optional: Create a default instance for easy import elsewhere
DEFAULT_DISPLAY_CONFIG = DisplayConfig()
