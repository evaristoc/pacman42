from pathlib import Path


def _find_env_directory() -> Path:
    basedir = Path(__file__).parent.parent.parent.parent
    env_dir = basedir / '.env'
    if env_dir.exists():
        return env_dir
    else:
        env_dir.mkdir()
    return env_dir


def get_db_path() -> str:
    env_dir = _find_env_directory()
    db_name = 'score.db'
    return str(env_dir / db_name)


if __name__ == '__main__':
    get_db_path()
