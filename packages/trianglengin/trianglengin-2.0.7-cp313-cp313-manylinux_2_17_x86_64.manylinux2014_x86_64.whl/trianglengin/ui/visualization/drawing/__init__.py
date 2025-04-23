"""Drawing functions for specific visual elements."""

# Guard UI imports
try:
    # Import the new utility function
    from .grid import (
        draw_debug_grid_overlay,
        draw_grid_background,
        draw_grid_state,
    )
    from .highlight import draw_debug_highlight
    from .hud import render_hud
    from .previews import (
        draw_floating_preview,
        draw_placement_preview,
        render_previews,
    )
    from .shapes import draw_shape
    from .utils import get_triangle_points

    __all__ = [
        "draw_grid_background",
        "draw_grid_state",
        "draw_debug_grid_overlay",
        "draw_shape",
        "render_previews",
        "draw_placement_preview",
        "draw_floating_preview",
        "render_hud",
        "draw_debug_highlight",
        "get_triangle_points",  # Export the helper
    ]

except ImportError as e:
    import warnings

    warnings.warn(
        f"Could not import UI drawing components ({e}). "
        "Ensure 'pygame' is installed (`pip install trianglengin[ui]`).",
        ImportWarning,
        stacklevel=2,
    )
    __all__ = []
