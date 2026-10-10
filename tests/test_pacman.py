from src.PacMan import PacMan


def test_pacman_exists() -> None:
    # captured = capsys.readouterr()
    assert str(PacMan()) == "I am PacMan!"
