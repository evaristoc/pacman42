import logging
from rich.logging import RichHandler


def setup() -> None:
    logging.basicConfig(
        level=getattr(logging, 'DEBUG', logging.DEBUG),
        # stream=sys.stdout,
        handlers=[RichHandler(rich_tracebacks=True,
                              markup=False)],
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
