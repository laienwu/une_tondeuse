from unittest.mock import MagicMock

import pytest

from tondeuse import Direction, Rotation
from tondeuse.mow import Mow, Position, Grid, GridPlacementException


def test_direction():
    t = Mow(Position(0, 0), Direction.E)
    t.direction = Direction.W
    assert t.direction in Direction
    assert t.position._x == 0
    assert t.position._y == 0

    t.position = Position(1, 1)
    assert t.position._x == 1
    assert t.position._y == 1

    t.rotate(Rotation.D)
    t.rotate(Rotation.D)
    assert t.direction == Direction.E

    t.rotate(Rotation.G)
    assert t.direction == Direction.N

    t.rotate(Rotation.G)
    assert t.direction == Direction.W


def test_move():
    m = Mow(Position(6, 6), Direction.W)
    # No associated grid
    with pytest.raises(GridPlacementException):
        m.advance()

    # Outside the grid
    g = Grid(0, 0, 5, 5)
    with pytest.raises(GridPlacementException):
        m.associate_to_grid(g)

    m.position = Position(1, 1)
    m.associate_to_grid(g)
    # Grid already associated
    with pytest.raises(GridPlacementException):
        m.associate_to_grid(g)

    m.advance()
    assert m.position._x == 0

    # On an edge, can't mve to the left
    m.advance()
    assert m.position._x == 0


def test_grid():
    g = Grid(0, 0, 5, 5)
    p = Position(-1, -1)
    assert g.is_inbound(p) is False


def test_path_execution():
    m = Mow(Position(0, 0), Direction.E)
    m.rotate = MagicMock()
    m.advance = MagicMock()
    m.execute_path("ABCDEFGH")

    assert m.rotate.call_count == 2
    m.advance.assert_called_once()


def test_instruction():
    g = Grid(0, 0, 5, 5)
    m1 = Mow(Position(1, 2), Direction.N)
    m1.associate_to_grid(g)
    m1.execute_path("GAGAGAGAA")
    assert "1 3 N" == str(m1)
    print(m1)

    m2 = Mow(Position(3, 3), Direction.E)
    m2.associate_to_grid(g)
    m2.execute_path("AADAADADDA")
    assert "5 1 E" == str(m2)
    print(m2)
