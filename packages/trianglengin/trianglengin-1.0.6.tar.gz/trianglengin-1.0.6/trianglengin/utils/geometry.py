def is_point_in_polygon(
    point: tuple[float, float], polygon: list[tuple[float, float]]
) -> bool:
    """
    Checks if a point is inside a polygon using the Winding Number algorithm.
    Handles points on the boundary correctly.

    Args:
        point: Tuple (x, y) representing the point coordinates.
        polygon: List of tuples [(x1, y1), (x2, y2), ...] representing polygon vertices in order.

    Returns:
        True if the point is inside or on the boundary of the polygon, False otherwise.
    """
    x, y = point
    n = len(polygon)
    if n < 3:  # Need at least 3 vertices for a polygon
        return False

    wn = 0  # the winding number counter
    epsilon = 1e-9  # Tolerance for floating point comparisons

    # loop through all edges of the polygon
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]  # Wrap around to the first vertex

        # Check if point is on the vertex P1
        if abs(p1[0] - x) < epsilon and abs(p1[1] - y) < epsilon:
            return True

        # Check if point is on the horizontal edge P1P2
        if (
            abs(p1[1] - p2[1]) < epsilon
            and abs(p1[1] - y) < epsilon
            and min(p1[0], p2[0]) - epsilon <= x <= max(p1[0], p2[0]) + epsilon
        ):
            return True

        # Check if point is on the vertical edge P1P2
        if (
            abs(p1[0] - p2[0]) < epsilon
            and abs(p1[0] - x) < epsilon
            and min(p1[1], p2[1]) - epsilon <= y <= max(p1[1], p2[1]) + epsilon
        ):
            return True

        # Check for intersection using winding number logic
        # Check y range (inclusive min, exclusive max for upward crossing)
        y_in_upward_range = p1[1] <= y + epsilon < p2[1] + epsilon
        y_in_downward_range = p2[1] <= y + epsilon < p1[1] + epsilon

        if y_in_upward_range or y_in_downward_range:
            # Calculate orientation: > 0 for left turn (counter-clockwise), < 0 for right turn
            orientation = (p2[0] - p1[0]) * (y - p1[1]) - (x - p1[0]) * (p2[1] - p1[1])

            if (
                y_in_upward_range and orientation > epsilon
            ):  # Upward crossing, P left of edge
                wn += 1
            elif (
                y_in_downward_range and orientation < -epsilon
            ):  # Downward crossing, P right of edge
                wn -= 1
            elif (
                abs(orientation) < epsilon
                and min(p1[0], p2[0]) - epsilon <= x <= max(p1[0], p2[0]) + epsilon
                and min(p1[1], p2[1]) - epsilon <= y <= max(p1[1], p2[1]) + epsilon
            ):
                return True  # Point is on the edge segment

    # wn == 0 only when P is outside
    return wn != 0
