"""Logger central da aplicação, baseado em `rich`."""

import logging

from rich.logging import RichHandler

LOGGER_NAME: str = "rpa_smart_news"


def setup_logger(level: str = "INFO") -> logging.Logger:
    """Configura e retorna o logger raiz da aplicação."""
    handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        show_time=True,
        markup=False,
    )
    logging.basicConfig(
        level=level.upper(),
        format="%(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[handler],
        force=True,
    )
    return logging.getLogger(LOGGER_NAME)


def get_logger() -> logging.Logger:
    """Retorna o logger nomeado da aplicação."""
    return logging.getLogger(LOGGER_NAME)
