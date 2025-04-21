# File: trianglengin/tests/core/structs/test_shape.py

# Import directly from the library being tested
from trianglengin.core.structs import Shape


def test_shape_initialization():
    """Test basic shape initialization."""
    triangles = [(0, 0, False), (1, 0, True)]
    color = (255, 0, 0)
    shape = Shape(triangles, color)
    assert shape.triangles == sorted(triangles)  # Check sorting
    assert shape.color == color


def test_shape_bbox():
    """Test bounding box calculation."""
    triangles1 = [(0, 0, False)]
    shape1 = Shape(triangles1, (1, 1, 1))
    assert shape1.bbox() == (0, 0, 0, 0)

    triangles2 = [(0, 1, True), (1, 0, False), (1, 2, False)]
    shape2 = Shape(triangles2, (2, 2, 2))
    assert shape2.bbox() == (0, 0, 1, 2)  # min_r, min_c, max_r, max_c

    shape3 = Shape([], (3, 3, 3))
    assert shape3.bbox() == (0, 0, 0, 0)


def test_shape_copy():
    """Test the copy method."""
    triangles = [(0, 0, False), (1, 0, True)]
    color = (255, 0, 0)
    shape1 = Shape(triangles, color)
    shape2 = shape1.copy()

    assert shape1 == shape2
    assert shape1 is not shape2
    assert shape1.triangles is not shape2.triangles  # List should be copied
    assert shape1.color is shape2.color  # Color tuple is shared (immutable)

    # Modify copy's triangle list
    shape2.triangles.append((2, 2, True))
    assert shape1.triangles != shape2.triangles


def test_shape_equality():
    """Test shape equality comparison."""
    t1 = [(0, 0, False)]
    c1 = (1, 1, 1)
    t2 = [(0, 0, False)]
    c2 = (1, 1, 1)
    t3 = [(0, 0, True)]
    c3 = (2, 2, 2)

    shape1 = Shape(t1, c1)
    shape2 = Shape(t2, c2)
    shape3 = Shape(t3, c1)
    shape4 = Shape(t1, c3)

    assert shape1 == shape2
    assert shape1 != shape3
    assert shape1 != shape4
    assert shape1 != "not a shape"


def test_shape_hash():
    """Test shape hashing."""
    t1 = [(0, 0, False)]
    c1 = (1, 1, 1)
    t2 = [(0, 0, False)]
    c2 = (1, 1, 1)
    t3 = [(0, 0, True)]

    shape1 = Shape(t1, c1)
    shape2 = Shape(t2, c2)
    shape3 = Shape(t3, c1)

    assert hash(shape1) == hash(shape2)
    assert hash(shape1) != hash(shape3)

    shape_set = {shape1, shape2, shape3}
    assert len(shape_set) == 2
