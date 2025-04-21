# File: src/trianglengin/utils/geometry.py
from collections.abc import Sequence  # Import Tuple


def is_point_in_polygon(
    point: tuple[float, float], polygon: Sequence[tuple[float, float]]
) -> bool:
    """
    Checks if a point is inside a polygon using the Winding Number algorithm.
    Handles points on the boundary correctly.

    Args:
        point: Tuple (x, y) representing the point coordinates.
        polygon: Sequence of tuples [(x1, y1), (x2, y2), ...] representing polygon vertices in order.

    Returns:
        True if the point is inside or on the boundary of the polygon, False otherwise.
    """
    x, y = point
    n = len(polygon)
    if n < 3:
        return False

    wn = 0
    epsilon = 1e-9

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        if abs(p1[0] - x) < epsilon and abs(p1[1] - y) < epsilon:
            return True
        if (
            abs(p1[1] - p2[1]) < epsilon
            and abs(p1[1] - y) < epsilon
            and min(p1[0], p2[0]) - epsilon <= x <= max(p1[0], p2[0]) + epsilon
        ):
            return True
        if (
            abs(p1[0] - p2[0]) < epsilon
            and abs(p1[0] - x) < epsilon
            and min(p1[1], p2[1]) - epsilon <= y <= max(p1[1], p2[1]) + epsilon
        ):
            return True

        y_in_upward_range = p1[1] <= y + epsilon < p2[1] + epsilon
        y_in_downward_range = p2[1] <= y + epsilon < p1[1] + epsilon

        if y_in_upward_range or y_in_downward_range:
            orientation = (p2[0] - p1[0]) * (y - p1[1]) - (x - p1[0]) * (p2[1] - p1[1])
            if y_in_upward_range and orientation > epsilon:
                wn += 1
            elif y_in_downward_range and orientation < -epsilon:
                wn -= 1
            elif (
                abs(orientation) < epsilon
                and min(p1[0], p2[0]) - epsilon <= x <= max(p1[0], p2[0]) + epsilon
                and min(p1[1], p2[1]) - epsilon <= y <= max(p1[1], p2[1]) + epsilon
            ):
                return True

    return wn != 0
