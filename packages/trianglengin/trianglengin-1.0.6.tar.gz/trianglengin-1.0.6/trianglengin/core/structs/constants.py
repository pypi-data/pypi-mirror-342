SHAPE_COLORS: list[tuple[int, int, int]] = [
    (220, 40, 40),  # 0: Red
    (60, 60, 220),  # 1: Blue
    (40, 200, 40),  # 2: Green
    (230, 230, 40),  # 3: Yellow
    (240, 150, 20),  # 4: Orange
    (140, 40, 140),  # 5: Purple
    (40, 200, 200),  # 6: Cyan
    (200, 100, 180),  # 7: Pink (Example addition)
    (100, 180, 200),  # 8: Light Blue (Example addition)
]

# --- NumPy GridData Color Representation ---
# ID for empty cells in the _color_id_np array
NO_COLOR_ID: int = -1
# ID for debug-toggled cells
DEBUG_COLOR_ID: int = -2

# Mapping from Color ID (int >= 0) to RGB tuple.
# Index 0 corresponds to SHAPE_COLORS[0], etc.
# This list is used by visualization to get the RGB from the ID.
COLOR_ID_MAP: list[tuple[int, int, int]] = SHAPE_COLORS

# Reverse mapping for efficient lookup during placement (Color Tuple -> ID)
# Note: Ensure SHAPE_COLORS have unique tuples.
COLOR_TO_ID_MAP: dict[tuple[int, int, int], int] = {
    color: i for i, color in enumerate(COLOR_ID_MAP)
}
