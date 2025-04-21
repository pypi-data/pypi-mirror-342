# File: trianglengin/core/structs/shape.py
from __future__ import annotations

import logging
from typing import cast

logger = logging.getLogger(__name__)


class Shape:
    """Represents a polyomino-like shape made of triangles."""

    def __init__(
        self, triangles: list[tuple[int, int, bool]], color: tuple[int, int, int]
    ):
        # Ensure triangles are tuples and sort them for consistent representation
        # Sorting is based on (row, col) primarily
        try:
            # Explicitly cast inner tuples to the correct type for mypy
            processed_triangles = [
                cast("tuple[int, int, bool]", tuple(t)) for t in triangles
            ]
            self.triangles: list[tuple[int, int, bool]] = sorted(processed_triangles)
        except Exception as e:
            logger.error(f"Failed to sort triangles: {triangles}. Error: {e}")
            # Fallback or re-raise depending on desired behavior
            self.triangles = [
                cast("tuple[int, int, bool]", tuple(t)) for t in triangles
            ]  # Store as is if sort fails

        self.color: tuple[int, int, int] = color

    def bbox(self) -> tuple[int, int, int, int]:
        """Calculates bounding box (min_r, min_c, max_r, max_c) in relative coords."""
        if not self.triangles:
            return (0, 0, 0, 0)
        rows = [t[0] for t in self.triangles]
        cols = [t[1] for t in self.triangles]
        return (min(rows), min(cols), max(rows), max(cols))

    def copy(self) -> Shape:
        """Creates a shallow copy (triangle list is copied, color is shared)."""
        new_shape = Shape.__new__(Shape)
        new_shape.triangles = list(self.triangles)
        new_shape.color = self.color
        return new_shape

    def __str__(self) -> str:
        return f"Shape(Color:{self.color}, Tris:{len(self.triangles)})"

    def __eq__(self, other: object) -> bool:
        """Checks for equality based on triangles and color."""
        if not isinstance(other, Shape):
            return NotImplemented
        # Compare sorted lists of tuples
        return self.triangles == other.triangles and self.color == other.color

    def __hash__(self) -> int:
        """Allows shapes to be used in sets/dicts if needed."""
        # Hash the tuple representation of the sorted list
        return hash((tuple(self.triangles), self.color))
