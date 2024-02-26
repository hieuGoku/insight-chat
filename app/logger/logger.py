"""Define logger for project."""

import logging


class UvicornFormatter(logging.Formatter):
    """Uvicorn Formatter."""

    FORMAT = (
        "\033[38;5;244m%(asctime)s\033[0m"
        " | "
        "%(levelname)-7s"
        " | "
        "\033[38;5;214m%(name)s\033[0m"
        " : "
        "\033[38;5;111m%(message)s\033[0m"
    )

    LEVEL_COLORS = {
        "DEBUG": "\033[38;5;33m",  # Light Blue for DEBUG
        "INFO": "\033[38;5;32m",  # Green for INFO
        "WARNING": "\033[38;5;220m",  # Orange/Yellow for WARNING
        "ERROR": "\033[38;5;196m",  # Red for ERROR
        "CRITICAL": "\033[48;5;196;38;5;231m",  # Red background, White text for CRITICAL
    }

    def format(self, record):
        """Config format"""
        levelname = record.levelname
        level_color = self.LEVEL_COLORS.get(levelname, "")
        record.levelname = f"{level_color}{levelname}\033[0m"
        return super().format(record)


def configure_logging():
    """
    The function `configure_logging` sets up logging in Python with a console handler and a specific log
    level.
    :return: a logger object.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    console_handler.setFormatter(UvicornFormatter(UvicornFormatter.FORMAT))

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)

    return logger


custom_logger = configure_logging()
