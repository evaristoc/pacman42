from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import Tile
from typing import Union
import heapq


class AStarError(Exception):
    pass


class AStarNode:
    def __init__(self, *,
                 prev_node: Union["AStarNode", None] = None,
                 move: tuple[int, int] | None = None,
                 steps: int,
                 target: tuple[int, int],
                 position: tuple[int, int] | None = None
                 ) -> None:
        self.prev_node: Union["AStarNode", None] = prev_node
        self.move: tuple[int, int] | None = move
        self.position = self._get_position(prev_node=prev_node,
                                           move=move,
                                           position=position)
        self.steps: int = steps
        self.distance_to_target = self._distance(self.position, target)
        self.priority: float = self._calculate_priority(steps,
                                                        self.distance_to_target
                                                        )

    def __lt__(self, other: 'AStarNode') -> bool:
        return self.priority < other.priority

    def _get_position(self, *,
                      prev_node: Union["AStarNode", None],
                      move: tuple[int, int] | None,
                      position: tuple[int, int] | None
                      ) -> tuple[int, int]:
        if position:
            return position
        else:
            if move and prev_node:
                return self._process_move(move,
                                          prev_node.position)
            else:
                raise ValueError("No position provided and no "
                                 "move/prev position at initiation "
                                 "of AStarNode.")

    @staticmethod
    def _distance(current_pos: tuple[int, int],
                  target: tuple[int, int]
                  ) -> float:
        x_current, y_current = current_pos
        x_target, y_target = target
        return abs(x_current - x_target) + abs(y_current - y_target)

    @staticmethod
    def _calculate_priority(steps: int, distance_to_target: float) -> float:
        return steps + 5 * distance_to_target

    @staticmethod
    def _process_move(move: tuple[int, int],
                      prev_position: tuple[int, int]
                      ) -> tuple[int, int]:
        dx, dy = move
        old_x, old_y = prev_position
        return (old_x + dx, old_y + dy)

    def __repr__(self) -> str:
        return (f"Position: ({self.position}), steps: {self.steps}, "
                f"distance: {self.distance_to_target}, "
                f"priority {self.priority}")


def AStar_next_move(
    position: tuple[int, int],
    target: tuple[int, int],
    maze: Maze
) -> tuple[int, int]:
    optimal_path_node = _find_path(position=position,
                                   target=target,
                                   maze=maze)
    if optimal_path_node:
        return _next_move(optimal_path_node=optimal_path_node)
    else:
        raise


def _find_path(position: tuple[int, int],
               target: tuple[int, int],
               maze: Maze) -> AStarNode | None:
    visited = set()
    steps = 0
    start_node = AStarNode(position=position,
                           steps=steps,
                           target=target,
                           )
    priority_queue: list[AStarNode] = list()
    heapq.heapify(priority_queue)
    heapq.heappush(priority_queue, start_node)
    while priority_queue:
        current = heapq.heappop(priority_queue)
        if current.position == target:
            return current
        if current.position in visited:
            continue

        visited.add(current.position)

        steps += 1
        successors = _generate_successors(current_node=current,
                                          maze=maze,
                                          steps=steps,
                                          target=target)
        for successor in successors:
            heapq.heappush(priority_queue, successor)
    return None


def _generate_successors(*, current_node: AStarNode,
                         maze: Maze,
                         steps: int,
                         target: tuple[int, int]
                         ) -> list[AStarNode]:
    current_pos_x, current_pos_y = current_node.position
    temp_tile: Tile | None = maze.grid[current_pos_y][current_pos_x]
    if temp_tile:
        possible_moves = temp_tile.get_open_walls()
    else:
        raise AStarError("The position of the current_node doesn't give a"
                         " valid Tile in the maze.")
    successors: list[AStarNode] = []
    for move in possible_moves:
        temp_node = AStarNode(prev_node=current_node,
                              move=move,
                              steps=steps,
                              target=target)
        successors.append(temp_node)
    return successors


def _next_move(optimal_path_node: AStarNode) -> tuple[int, int]:
    current = optimal_path_node
    while not current.steps == 1:
        if current.prev_node:
            current = current.prev_node
        else:
            raise ValueError(
                "Node with steps > 1 doesn't have a previous node.")
    if current.move:
        return current.move
    else:
        raise ValueError(
            "Node with steps == 1 doesn't have a move.")
