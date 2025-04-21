# File: trianglengin/tests/core/structs/test_triangle.py

# Import directly from the library being tested
from trianglengin.core.structs import Triangle


def test_triangle_initialization():
    """Test basic triangle initialization."""
    tri1 = Triangle(row=1, col=2, is_up=True)
    assert tri1.row == 1
    assert tri1.col == 2
    assert tri1.is_up
    assert not tri1.is_death
    assert not tri1.is_occupied
    assert tri1.color is None

    tri2 = Triangle(row=3, col=4, is_up=False, is_death=True)
    assert tri2.row == 3
    assert tri2.col == 4
    assert not tri2.is_up
    assert tri2.is_death
    assert tri2.is_occupied  # Occupied because it's death
    assert tri2.color is None


def test_triangle_copy():
    """Test the copy method."""
    tri1 = Triangle(row=1, col=2, is_up=True)
    tri1.is_occupied = True
    tri1.color = (255, 0, 0)
    tri1.neighbor_left = Triangle(1, 1, False)  # Add a neighbor

    tri2 = tri1.copy()

    assert tri1 == tri2
    assert tri1 is not tri2
    assert tri2.row == 1
    assert tri2.col == 2
    assert tri2.is_up
    assert tri2.is_occupied
    assert tri2.color == (255, 0, 0)
    assert not tri2.is_death
    # Neighbors should not be copied
    assert tri2.neighbor_left is None
    assert tri2.neighbor_right is None
    assert tri2.neighbor_vert is None

    # Modify copy and check original
    tri2.is_occupied = False
    tri2.color = (0, 255, 0)
    assert tri1.is_occupied
    assert tri1.color == (255, 0, 0)


def test_triangle_equality():
    """Test triangle equality based on row and col."""
    tri1 = Triangle(1, 2, True)
    tri2 = Triangle(1, 2, False)  # Different orientation/state
    tri3 = Triangle(1, 3, True)
    tri4 = Triangle(2, 2, True)

    assert tri1 == tri2  # Equality only checks row/col
    assert tri1 != tri3
    assert tri1 != tri4
    assert tri1 != "not a triangle"


def test_triangle_hash():
    """Test triangle hashing based on row and col."""
    tri1 = Triangle(1, 2, True)
    tri2 = Triangle(1, 2, False)
    tri3 = Triangle(1, 3, True)

    assert hash(tri1) == hash(tri2)
    assert hash(tri1) != hash(tri3)

    tri_set = {tri1, tri2, tri3}
    assert len(tri_set) == 2  # tri1 and tri2 hash the same


def test_triangle_get_points():
    """Test vertex point calculation."""
    # Up triangle at origin (0,0) with cell width/height 100
    tri_up = Triangle(0, 0, True)
    pts_up = tri_up.get_points(ox=0, oy=0, cw=100, ch=100)
    # Expected: [(0, 100), (100, 100), (50, 0)]
    assert pts_up == [(0.0, 100.0), (100.0, 100.0), (50.0, 0.0)]

    # Down triangle at (1,1) with cell width/height 50, offset (10, 20)
    tri_down = Triangle(1, 1, False)
    # ox = 10, oy = 20, cw = 50, ch = 50
    # Base x = 10 + 1 * (50 * 0.75) = 10 + 37.5 = 47.5
    # Base y = 20 + 1 * 50 = 70
    pts_down = tri_down.get_points(ox=10, oy=20, cw=50, ch=50)
    # Expected: [(47.5, 70), (47.5+50, 70), (47.5+25, 70+50)]
    # Expected: [(47.5, 70.0), (97.5, 70.0), (72.5, 120.0)]
    assert pts_down == [(47.5, 70.0), (97.5, 70.0), (72.5, 120.0)]
