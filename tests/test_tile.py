from src.PacMan.game_logic.ingame.maze.tile import PelletState, Tile


def test_eating_pellet_clears_tile() -> None:
    tile = Tile(tilebyte=0, x=0, y=0)

    assert tile.pellet_state is PelletState.NORMALPELLET

    tile.pellet_eaten_by_pacman()

    assert tile.pellet_state is PelletState.NOPELLET
