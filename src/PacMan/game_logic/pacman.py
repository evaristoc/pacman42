from .entities import GameEntity


class Pacman(GameEntity):
    def __init__(self) -> None:
        self.spawn_point = self._get_spawn_point()

    def update(self, delta_time: float) -> None:
        pass

    def render(self) -> None:
        pass

    def get_position(self) -> tuple[float, float]:
        return (0, 0)  # TODO

    def _get_spawn_point(self) -> tuple[float, float]:
        """Returns the entity's spawn point as (x, y).

        Returns:
            A tuple of (x, y) coordinates representing the entity's spawnpoint
            in world space.
        """
        return (0, 0)  # TODO
