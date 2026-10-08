from abc import ABC, abstractmethod


class GameEntity(ABC):
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """
        Update the entity's state for the current frame.

        This method is called once per game loop iteration and should handle
        all state changes for this entity, such as movement, animation,
        collision detection, or AI logic.

        Args:
            delta_time (float): Time elapsed since the last frame, in seconds.
                Use this to ensure frame-rate-independent movement
                (e.g., position += velocity * delta_time).

        Returns:
            None
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """Render the entity to the screen.

        This method is called once per frame after all entities have updated.
        Implement drawing logic here (e.g., blit sprites, draw rectangles).
        """
        pass

    @abstractmethod
    def get_position(self) -> tuple[float, float]:
        """Return the entity's current position as (x, y).

        Returns:
            A tuple of (x, y) coordinates representing the entity's position
            in world space.
        """
        pass

    @abstractmethod
    def _get_spawn_point(self) -> tuple[float, float]:
        """Returns the entity's spawn point as (x, y).

        Returns:
            A tuple of (x, y) coordinates representing the entity's spawnpoint
            in world space.
        """
        pass
