from enum import Enum


class WallState(Enum):
    OPEN = 1
    NORMALWALL = 2
    OUTERWALL = 3


class Tile:
    def __init__(self, tilebyte: int, x: int, y: int) -> None:
        self.tilebyte = tilebyte
        self.wall_north: WallState = WallState.OPEN
        self.wall_south: WallState = WallState.OPEN
        self.wall_west: WallState = WallState.OPEN
        self.wall_east: WallState = WallState.OPEN
        self.cell_position_x: int = x
        self.cell_position_y: int = y

        self._set_open_walls_from_tilebyte()

    @property
    def tilebyte(self) -> int:
        return self._tilebyte

    @tilebyte.setter
    def tilebyte(self, tilebyte: int) -> None:
        if not isinstance(tilebyte, int):
            raise ValueError("Tilebyte is not a valid integer.")
        if tilebyte < 0 or tilebyte > 255:
            raise ValueError("Passed tilebyte to Tile-class "
                             "that is not in range 0-255.")
        self._tilebyte = tilebyte

    def _set_open_walls_from_tilebyte(self) -> None:
        if self.tilebyte & 1:
            self.wall_north = WallState.NORMALWALL
        if self.tilebyte & 2:
            self.wall_east = WallState.NORMALWALL
        if self.tilebyte & 4:
            self.wall_south = WallState.NORMALWALL
        if self.tilebyte & 8:
            self.wall_west = WallState.NORMALWALL
        if self.tilebyte & 16:
            self.wall_north = WallState.OUTERWALL
        if self.tilebyte & 32:
            self.wall_east = WallState.OUTERWALL
        if self.tilebyte & 64:
            self.wall_south = WallState.OUTERWALL
        if self.tilebyte & 128:
            self.wall_west = WallState.OUTERWALL

    def __repr__(self):
        return (f"N: {self.wall_north.value}, E: {self.wall_east.value}, "
                f"S: {self.wall_south.value}, W: {self.wall_west.value}")
