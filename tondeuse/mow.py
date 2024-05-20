from dataclasses import dataclass
from typing import Self, Optional, Tuple

from tondeuse import Direction, Rotation


class Position:
    """
    A class to represent a coordinate position in 2D space (grid).

    Attributes:
    -----------
    _x : int
        The x-coordinate of the position.
    _y : int
        The y-coordinate of the position.

    Methods:
    --------
    __init__(x: int, y: int):
        Initializes the position with x and y coordinates.

    __add__(pos: Self) -> 'Position':
        Returns a new Position instance representing the sum of coordinates to the initial position .
    """

    def __init__(self, x: int, y: int):
        """
        Initialize a new Position instance.

        Parameters:
        -----------
        x : int
            The x-coordinate of the position.
        y : int
            The y-coordinate of the position.
        """
        self._x = x
        self._y = y

    def __add__(self, pos: Self) -> "Position":
        """
        Add two Position instances.

        This method returns a new Position instance whose coordinates are the sum
        of the coordinates of this instance and another Position instance.

        Parameters:
        -----------
        pos : Position
            Another Position instance to add to this instance.

        Returns:
        --------
        Position
            A new Position instance with coordinates that are the sum of the coordinates
            of this instance and the input Position instance.
        """
        return Position(self._x + pos._x, self._y + pos._y)

    @property
    def coordinate(self) -> Tuple[int, int]:
        return self._x, self._y


@dataclass
class Grid:
    _x_min: int
    _y_min: int
    _x_max: int
    _y_max: int

    def is_inbound(self, pos: Position) -> bool:
        x, y = pos.coordinate
        return self._x_min <= x <= self._x_max and self._y_min <= y <= self._y_max


class GridPlacementException(Exception):
    """"""


class Mow:
    """
    A class to represent a mower with a position and direction on a grid (if associated to a grid).

    Attributes:
    -----------
    _position : Position
        The current position of the mower.
    _direction : Direction
        The current direction the mower is facing.
    _grid : Optional[Grid]
        The grid to which the mower is associated.
    """

    def __init__(self, position: Position, direction: Direction):
        """
        Initialize a new Mow instance.

        Parameters:
        -----------
        position : Position
            The initial position of the mower.
        direction : Direction
            The initial direction the mower is facing.
        """
        self._position = position
        self._direction = direction
        self._grid: Optional[Grid] = None

    def __str__(self) -> str:
        x, y = self._position.coordinate
        return f"{x} {y} {self.direction.name}"

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, pos: Position) -> None:
        self._position = pos

    @property
    def direction(self) -> Direction:
        return self._direction

    @direction.setter
    def direction(self, direction: Direction) -> None:
        self._direction = direction

    def rotate(self, way: Rotation) -> None:
        """
        Rotate the mower in the specified direction.

        Parameters:
        -----------
        way : Rotation
            The rotation direction, which alters the current direction of the mower.
        """
        self._direction = Direction(
            (self._direction + way) % 4
        )  # Rely on the intEnum to compute the direction

    def associate_to_grid(self, grid: Grid) -> None:
        """
        Associate the mower to a grid.

        Parameters:
        -----------
        grid : Grid
            The grid to associate the mower with.

        Raises:
        -------
        GridPlacementException
            If the position does not belong to the grid or if the mower is already associated with a grid.
        """
        if not grid.is_inbound(self._position):
            raise GridPlacementException("Position does not belong to grid")
        if self._grid is not None:
            raise GridPlacementException("One grid is already set")

        self._grid = grid

    def advance(self) -> None:
        """
        Advance the mower one step in its current direction.

        Raises:
        -------
        GridPlacementException
            If the mower is not associated with any grid.

        Updates the mower's position if the new position is within the grid bounds.
        """
        if self._grid is None:
            raise GridPlacementException("No associated grid")

        match self._direction:
            case Direction.N:
                p = self._position + Position(0, 1)
            case Direction.E:
                p = self._position + Position(1, 0)
            case Direction.S:
                p = self._position + Position(0, -1)
            case Direction.W:
                p = self._position + Position(-1, 0)

        # noinspection PyUnboundLocalVariable
        if self._grid.is_inbound(p):
            self.position = p

    def execute_path(self, path: str) -> None:
        """
        Execute a sequence of commands to move and rotate the mower.

        Parameters:
        -----------
        path : str
            A string containing a sequence of commands ('G', 'D', 'A') to execute.

        Executes rotation ('G', 'D') and advancement ('A') commands sequentially.
        """
        for i in path:
            match i:
                # TODO: Should test the value against the Rotation enum keys
                case "G" | "D":
                    self.rotate(Rotation[i])
                case "A":
                    self.advance()
                case _:
                    pass
            pass
