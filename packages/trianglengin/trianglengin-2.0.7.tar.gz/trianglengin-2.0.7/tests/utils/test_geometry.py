# File: tests/utils/test_geometry.py

from trianglengin.utils import geometry


def test_is_point_in_polygon_square() -> None:
    """Test point in polygon for a simple square."""
    # Explicitly type as list of float tuples
    square: list[tuple[float, float]] = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert geometry.is_point_in_polygon((0.5, 0.5), square)
    assert geometry.is_point_in_polygon((0.5, 0.0), square)
    assert geometry.is_point_in_polygon((1.0, 0.5), square)
    assert geometry.is_point_in_polygon((0.5, 1.0), square)
    assert geometry.is_point_in_polygon((0.0, 0.5), square)
    assert geometry.is_point_in_polygon((0.0, 0.0), square)
    assert geometry.is_point_in_polygon((1.0, 1.0), square)
    assert geometry.is_point_in_polygon((1.0, 0.0), square)
    assert geometry.is_point_in_polygon((0.0, 1.0), square)
    assert not geometry.is_point_in_polygon((1.5, 0.5), square)
    assert not geometry.is_point_in_polygon((0.5, -0.5), square)
    assert not geometry.is_point_in_polygon((-0.1, 0.1), square)
    assert not geometry.is_point_in_polygon((0.5, 1.1), square)


def test_is_point_in_polygon_triangle() -> None:
    """Test point in polygon for a triangle."""
    triangle: list[tuple[float, float]] = [(0.0, 0.0), (2.0, 0.0), (1.0, 2.0)]
    assert geometry.is_point_in_polygon((1.0, 0.5), triangle)
    assert geometry.is_point_in_polygon((1.0, 1.0), triangle)
    assert geometry.is_point_in_polygon((1.0, 0.0), triangle)
    assert geometry.is_point_in_polygon((0.5, 1.0), triangle)
    assert geometry.is_point_in_polygon((1.5, 1.0), triangle)
    assert geometry.is_point_in_polygon((0.0, 0.0), triangle)
    assert geometry.is_point_in_polygon((2.0, 0.0), triangle)
    assert geometry.is_point_in_polygon((1.0, 2.0), triangle)
    assert not geometry.is_point_in_polygon((1.0, 2.1), triangle)
    assert not geometry.is_point_in_polygon((3.0, 0.5), triangle)
    assert not geometry.is_point_in_polygon((-0.5, 0.5), triangle)
    assert not geometry.is_point_in_polygon((1.0, -0.1), triangle)


def test_is_point_in_polygon_concave() -> None:
    """Test point in polygon for a concave shape (e.g., Pacman)."""
    # Cast int tuples to float tuples for the test data
    concave: list[tuple[float, float]] = [
        (float(x), float(y))
        for x, y in [(0, 0), (3, 0), (3, 1), (1, 1), (1, 2), (2, 2), (2, 3), (0, 3)]
    ]
    assert geometry.is_point_in_polygon((0.5, 0.5), concave)
    assert geometry.is_point_in_polygon((2.5, 0.5), concave)
    assert geometry.is_point_in_polygon((0.5, 2.5), concave)
    assert geometry.is_point_in_polygon((1.5, 2.5), concave)
    assert not geometry.is_point_in_polygon((1.5, 1.5), concave)
    assert not geometry.is_point_in_polygon((4.0, 1.0), concave)
    assert not geometry.is_point_in_polygon((1.0, 4.0), concave)
    assert geometry.is_point_in_polygon((1.5, 0.0), concave)
    assert geometry.is_point_in_polygon((1.0, 1.5), concave)
    assert geometry.is_point_in_polygon((1.5, 1.0), concave)
    assert geometry.is_point_in_polygon((2.0, 2.5), concave)
    assert geometry.is_point_in_polygon((0.0, 1.5), concave)
    assert geometry.is_point_in_polygon((1.0, 1.0), concave)
    assert geometry.is_point_in_polygon((1.0, 2.0), concave)
    assert geometry.is_point_in_polygon((3.0, 0.0), concave)
    assert geometry.is_point_in_polygon((0.0, 3.0), concave)
