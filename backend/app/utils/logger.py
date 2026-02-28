import logging


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging.
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get named logger instance.
    """
    return logging.getLogger(name)