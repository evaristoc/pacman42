from src.PacMan.game_logic.gamemanager.gamelogicmng import GameLogicManager
from src.PacMan.game_logic.ingame.characters.ghosts.ghosts import GhostManager, GhostName
from src.PacMan.game_logic.ingame.characters.ghosts.ghostsm import (ChasingGhostState,
                                                                    FrightenedGhostState)
from src.PacMan.game_logic.ingame.collision import CollisionManager
from src.PacMan.game_logic.ingame.maze.maze import Maze
from src.PacMan.game_logic.ingame.maze.tile import PelletState
from src.PacMan.game_logic.ingame.characters.pacman import Pacman
from src.PacMan.game_logic.player import Player
from src.PacMan.game_logic.score_mng import ScoreManager
from src.PacMan.game_logic.ingame.time.time import TimeManager
from src.PacMan.validation_contracts.event_enums import InGameEvents


def build_collision_manager() -> CollisionManager:
    maze = Maze([[0 for _ in range(5)] for _ in range(5)])
    player = Player(name="Ada")
    pacman = Pacman(maze, speed=1)
    ghostmng = GhostManager(maze, speed=1)
    pacman.position = maze.return_tile_from_position(position=(2, 2))
    return CollisionManager(
        maze=maze,
        pacman=pacman,
        ghostmng=ghostmng,
        player=player,
        timemng=TimeManager(),
        scoremng=ScoreManager(player),
    )


def test_pacman_eats_a_normal_pellet() -> None:
    collision = build_collision_manager()
    tile = collision.pacman.position

    collision.check_pacman_pellet_collisions()

    assert tile.pellet_state.name == "NOPELLET"
    assert collision.player.score == 50


def test_ghost_collision_while_frightened_scores_and_eats_ghost() -> None:
    collision = build_collision_manager()
    ghost = collision.ghostmng.ghosts[GhostName.BLINKY]
    ghost.position = collision.pacman.position.get_position_from_tile()
    ghost.state = FrightenedGhostState(ghost.strategy)

    collision.check_pacman_ghost_collisions()

    assert collision.player.score == 200
    assert ghost.state.__class__.__name__ == "EatenGhostState"


def test_power_pellet_activates_ghost_frightened_state() -> None:
    collision = build_collision_manager()
    tile = collision.pacman.position
    tile.pellet_state = PelletState.POWERPELLET

    collision.check_pacman_pellet_collisions()

    assert tile.pellet_state.name == "NOPELLET"
    assert collision.player.score == 100
    for ghost in collision.ghostmng.ghosts.values():
        assert ghost.state.__class__.__name__ == "FrightenedGhostState"


def test_ghost_collision_without_frightened_state_loses_a_life() -> None:
    collision = build_collision_manager()
    ghost = collision.ghostmng.ghosts[GhostName.BLINKY]
    ghost.position = collision.pacman.position.get_position_from_tile()
    ghost.state = ChasingGhostState(ghost.strategy, speed=1)

    class DummyTimeManager:
        def restart_countdown(self) -> None:
            return None

    collision.timemng = DummyTimeManager()

    collision.check_pacman_ghost_collisions()

    assert collision.player.lives == 2
    assert collision.pacman.position == collision.pacman.spawn_point


def test_ingame_pause_toggles_without_a_separate_pause_state() -> None:
    manager = GameLogicManager()

    manager.update_logic({InGameEvents.PAUSE: None})
    assert manager.state.__class__.__name__ == "InGameState"
    assert manager.state.paused is True

    manager.update_logic({InGameEvents.PAUSE: None})
    assert manager.state.paused is False
