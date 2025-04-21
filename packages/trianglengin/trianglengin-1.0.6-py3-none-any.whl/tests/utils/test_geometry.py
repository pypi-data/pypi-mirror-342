# File: trianglengin/tests/utils/test_geometry.py

# Import directly from the library being tested
from trianglengin.utils import geometry


def test_is_point_in_polygon_square():
    """Test point in polygon for a simple square."""
    square = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

    # Inside
    assert geometry.is_point_in_polygon((0.5, 0.5), square)

    # On edge
    assert geometry.is_point_in_polygon((0.5, 0.0), square)
    assert geometry.is_point_in_polygon((1.0, 0.5), square)
    assert geometry.is_point_in_polygon((0.5, 1.0), square)
    assert geometry.is_point_in_polygon((0.0, 0.5), square)

    # On vertex
    assert geometry.is_point_in_polygon((0.0, 0.0), square)
    assert geometry.is_point_in_polygon((1.0, 1.0), square)
    assert geometry.is_point_in_polygon((1.0, 0.0), square)
    assert geometry.is_point_in_polygon((0.0, 1.0), square)

    # Outside
    assert not geometry.is_point_in_polygon((1.5, 0.5), square)
    assert not geometry.is_point_in_polygon((0.5, -0.5), square)
    assert not geometry.is_point_in_polygon((-0.1, 0.1), square)
    assert not geometry.is_point_in_polygon((0.5, 1.1), square)  # Added top outside


def test_is_point_in_polygon_triangle():
    """Test point in polygon for a triangle."""
    triangle = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]

    # Inside
    assert geometry.is_point_in_polygon((1.0, 0.5), triangle)
    assert geometry.is_point_in_polygon((1.0, 1.0), triangle)

    # On edge
    assert geometry.is_point_in_polygon((1.0, 0.0), triangle)  # Base
    assert geometry.is_point_in_polygon((0.5, 1.0), triangle)  # Left edge
    assert geometry.is_point_in_polygon((1.5, 1.0), triangle)  # Right edge

    # On vertex
    assert geometry.is_point_in_polygon((0.0, 0.0), triangle)
    assert geometry.is_point_in_polygon((2.0, 0.0), triangle)
    assert geometry.is_point_in_polygon((1.0, 2.0), triangle)

    # Outside
    assert not geometry.is_point_in_polygon((1.0, 2.1), triangle)
    assert not geometry.is_point_in_polygon((3.0, 0.5), triangle)
    assert not geometry.is_point_in_polygon((-0.5, 0.5), triangle)
    assert not geometry.is_point_in_polygon((1.0, -0.1), triangle)


def test_is_point_in_polygon_concave():
    """Test point in polygon for a concave shape (e.g., Pacman)."""
    # Simple concave shape (like a U)
    concave = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 2), (2, 2), (2, 3), (0, 3)]

    # Inside
    assert geometry.is_point_in_polygon((0.5, 0.5), concave)
    assert geometry.is_point_in_polygon((2.5, 0.5), concave)
    assert geometry.is_point_in_polygon((0.5, 2.5), concave)
    assert geometry.is_point_in_polygon((1.5, 2.5), concave)  # Inside the 'U' part

    # Outside (in the 'mouth')
    assert not geometry.is_point_in_polygon((1.5, 1.5), concave)

    # Outside (general)
    assert not geometry.is_point_in_polygon((4.0, 1.0), concave)
    assert not geometry.is_point_in_polygon((1.0, 4.0), concave)

    # On edge
    assert geometry.is_point_in_polygon((1.5, 0.0), concave)
    assert geometry.is_point_in_polygon(
        (1.0, 1.5), concave
    )  # On the inner vertical edge
    assert geometry.is_point_in_polygon(
        (1.5, 1.0), concave
    )  # On the inner horizontal edge
    assert geometry.is_point_in_polygon(
        (2.0, 2.5), concave
    )  # On the outer vertical edge
    assert geometry.is_point_in_polygon((0.0, 1.5), concave)  # On outer edge

    # On vertex
    assert geometry.is_point_in_polygon((1.0, 1.0), concave)  # Inner corner
    assert geometry.is_point_in_polygon((1.0, 2.0), concave)  # Inner corner
    assert geometry.is_point_in_polygon((3.0, 0.0), concave)  # Outer corner
    assert geometry.is_point_in_polygon((0.0, 3.0), concave)  # Outer corner
