"""Utility functions for the drawing module."""


def get_triangle_points(
    r: int, c: int, is_up: bool, ox: float, oy: float, cw: float, ch: float
) -> list[tuple[float, float]]:
    """
    Calculates vertex points for drawing a triangle, relative to origin (ox, oy).
    """
    # Top-left corner of the bounding rectangle for the cell (r, c)
    # Note the horizontal offset depends only on column (c * 0.75 * cw)
    # Note the vertical offset depends only on row (r * ch)
    x = ox + c * (cw * 0.75)
    y = oy + r * ch

    if is_up:
        # Points for an upward-pointing triangle (base at bottom)
        # Vertices: Bottom-left, Bottom-right, Top-middle
        return [(x, y + ch), (x + cw, y + ch), (x + cw / 2, y)]
    else:
        # Points for a downward-pointing triangle (base at top)
        # Vertices: Top-left, Top-right, Bottom-middle
        return [(x, y), (x + cw, y), (x + cw / 2, y + ch)]
