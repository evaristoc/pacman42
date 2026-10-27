from enum import Enum


class WallState(Enum):
    """Defines the possible states of a wall on a tile face."""
    OPEN = 1
    NORMALWALL = 2
    OUTERWALL = 3


class PelletState(Enum):
    """Defines the possible states of a pellet on a tile."""
    NOPELLET = 0
    NORMALPELLET = 1
    POWERPELLET = 2


class TileBits(Enum):
    """Bitmasks used to determine wall states from a tilebyte.

    Bits 0-3 represent normal walls, and bits 4-7 represent outer boundaries.
    """
    NORTH_NORMAL = 1
    EAST_NORMAL = 2
    SOUTH_NORMAL = 4
    WEST_NORMAL = 8
    NORTH_OUTER = 16
    EAST_OUTER = 32
    SOUTH_OUTER = 64
    WEST_OUTER = 128


class TileError(Exception):
    pass


class Tile:
    """Represents a single cell in the maze.

    Parses a tilebyte to determine the state (Open, Normal Wall, or Outer Wall)
    of each of its four faces.
    """

    def __init__(self, tilebyte: int, x: int, y: int) -> None:
        self.tilebyte = tilebyte
        self.wall_north: WallState = WallState.OPEN
        self.wall_south: WallState = WallState.OPEN
        self.wall_west: WallState = WallState.OPEN
        self.wall_east: WallState = WallState.OPEN
        self.pellet_state: PelletState = PelletState.NORMALPELLET
        self.cell_position_x: int = x
        self.cell_position_y: int = y

        self._set_open_walls_from_tilebyte()
        self.pellet_state = self._set_pellet_state_from_tilebyte()

    @property
    def tilebyte(self) -> int:
        """The raw integer byte representation of the tile's walls."""
        return self._tilebyte

    @tilebyte.setter
    def tilebyte(self, tilebyte: int) -> None:
        """Sets the tilebyte after validating it is an integer
        between 0 and 255.

        Args:
            tilebyte: The integer value to set.

        Raises:
            ValueError: If the value is not an integer or
            is outside the 0-255 range.
        """
        if not isinstance(tilebyte, int):
            raise ValueError("Tilebyte is not a valid integer.")
        if tilebyte < 0 or tilebyte > 255:
            raise ValueError("Passed tilebyte to Tile-class "
                             "that is not in range 0-255.")
        self._tilebyte = tilebyte

    def get_open_walls(self) -> list[tuple[int, int]]:
        open_walls = []
        if self.wall_north == WallState.OPEN:
            open_walls.append((0, -1))
        if self.wall_east == WallState.OPEN:
            open_walls.append((1, 0))
        if self.wall_south == WallState.OPEN:
            open_walls.append((0, 1))
        if self.wall_west == WallState.OPEN:
            open_walls.append((-1, 0))
        return open_walls

    def get_position_from_tile(self) -> tuple[int, int]:
        return (self.cell_position_x, self.cell_position_y)

    def _set_open_walls_from_tilebyte(self) -> None:
        """Updates WallState properties based on the bits set in tilebyte.

        Normal wall bits are checked first, then outer boundary bits,
        ensuring outer walls take precedence.
        """
        if self.tilebyte & TileBits.NORTH_NORMAL.value:
            self.wall_north = WallState.NORMALWALL

        if self.tilebyte & TileBits.EAST_NORMAL.value:
            self.wall_east = WallState.NORMALWALL

        if self.tilebyte & TileBits.SOUTH_NORMAL.value:
            self.wall_south = WallState.NORMALWALL

        if self.tilebyte & TileBits.WEST_NORMAL.value:
            self.wall_west = WallState.NORMALWALL

        if self.tilebyte & TileBits.NORTH_OUTER.value:
            self.wall_north = WallState.OUTERWALL

        if self.tilebyte & TileBits.EAST_OUTER.value:
            self.wall_east = WallState.OUTERWALL

        if self.tilebyte & TileBits.SOUTH_OUTER.value:
            self.wall_south = WallState.OUTERWALL

        if self.tilebyte & TileBits.WEST_OUTER.value:
            self.wall_west = WallState.OUTERWALL

    def _set_pellet_state_from_tilebyte(self) -> PelletState:
        if self.tilebyte.bit_count() == 4:
            print(self)
            return PelletState.NOPELLET
        temporary_tilebyte = self.tilebyte >> 4 & 0x0F
        if temporary_tilebyte.bit_count() > 1:
            return PelletState.POWERPELLET
        return PelletState.NORMALPELLET

    def pellet_eaten_by_pacman(self) -> None:
        self.pellet_state = PelletState.NOPELLET

    def has_pellet(self) -> bool:
        if self.pellet_state == PelletState.NOPELLET:
            return False
        return True

    def __repr__(self) -> str:
        """Returns a string representation of the wall states for each face."""
        return (f"N;{self.wall_north.value},E:{self.wall_east.value},"
                f"S:{self.wall_south.value},W:{self.wall_west.value}")
