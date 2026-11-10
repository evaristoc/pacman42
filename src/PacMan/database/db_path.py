from pathlib import Path
from src.PacMan.app_config.config import DATABASE_NAME, DATABASE_DIR


def _find_env_directory() -> Path:
    basedir = Path(__file__).parent.parent.parent.parent
    env_dir = basedir / DATABASE_DIR
    if env_dir.exists():
        return env_dir
    else:
        env_dir.mkdir()
    return env_dir


def get_db_path() -> str:
    env_dir = _find_env_directory()
    db_name = DATABASE_NAME
    return str(env_dir / db_name)


if __name__ == '__main__':
    get_db_path()
