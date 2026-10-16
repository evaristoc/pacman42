from mazegenerator import MazeGenerator
from src.PacMan.game_logic.map.tile import Tile
from typing import Union


class Map:
    def __init__(self, maze: list[list]) -> None:
        self.height = len(maze)
        self.width = len(maze[0])
        self.outerbound_maze = self._find_outerbounds(maze)
        self.grid: list[list[Tile | None]] = self._build_grid()

    def _find_outerbounds(self, maze: list[list]) -> list[list]:
        outerbound_maze = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        for i, _ in enumerate(range(self.height)):
            for j, _ in enumerate(range(self.width)):
                temp_var = maze[i][j]
                if temp_var < 0 or temp_var > 15:
                    raise ValueError("Invalid value in maze passed to "
                                     "self._find_outerbounds() in Map-class")

                # Adding to the bitmask to account for outer bounds of the map
                if i == 0:
                    temp_var += (16 - 1)
                if j == self.width - 1:
                    temp_var += (32 - 2)
                if i == self.height - 1:
                    temp_var += (64 - 4)
                if j == 0:
                    temp_var += (128 - 8)

                outerbound_maze[i][j] = temp_var

        return outerbound_maze

    def _build_grid(self) -> list[list[Tile | None]]:

        grid: list[list[Union[None | Tile]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

        for i, _ in enumerate(range(self.height)):  # rows?
            for j, _ in enumerate(range(self.width)):  # cols?
                grid[j][i] = Tile(self.outerbound_maze[j][i], i, j)
        return grid

    def __repr__(self):
        result = str()
        for i, _ in enumerate(range(self.height)):
            if i > 0:
                result += '\n'
            for j, _ in enumerate(range(self.width)):
                if j < self.width - 1:
                    result += (str(self.grid[i][j]) + '   |    ')
                else:
                    result += str(self.grid[i][j])
        return result


class MapFactory:
    def __init__(self, nb_cells: int):
        self.mazegen = MazeGenerator(size=(nb_cells, nb_cells),
                                     perfect=True,
                                     seed=42)

    def make_map(self) -> Map:
        return Map(self.mazegen.maze)

# if __name__ == '__main__':
#     factory = MapFactory()
#     map = factory.make_map()
#     print(map)
