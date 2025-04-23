"""Core visualization components: renderers, layout, fonts, colors, coordinate mapping."""

# Direct imports - if pygame is missing, these will fail, which is intended behavior
# for the optional UI package.
from . import colors, coord_mapper, fonts, layout  # Import modules needed by others

# Visualizer is NOT exported from here to avoid circular imports.
# Import it directly: from trianglengin.ui.visualization.core.visualizer import Visualizer

__all__ = [
    # "Visualizer", # REMOVED
    "layout",
    "fonts",
    "colors",
    "coord_mapper",
]
