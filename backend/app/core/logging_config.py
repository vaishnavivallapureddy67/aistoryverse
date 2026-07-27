import logging
import sys
from app.core.config import settings

def setup_logging():
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

    # Configure app loggers
    app_logger = logging.getLogger("ai_storyverse")
    app_logger.setLevel(log_level)

    logger = logging.getLogger("ai_storyverse.system")
    logger.info(f"Centralized Logging Initialized for {settings.PROJECT_NAME} (Level: {logging.getLevelName(log_level)})")

setup_logging()
logger = logging.getLogger("ai_storyverse.system")
