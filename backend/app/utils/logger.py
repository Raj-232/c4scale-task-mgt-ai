import logging
from logging.config import dictConfig

# ANSI color codes for log levels
class CustomFormatter(logging.Formatter):
    """Custom formatter to color only the log level text."""
    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[32m",     # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[1;31m"  # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"  # Color only log level
        return super().format(record)

# Define the logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": CustomFormatter,
            "format": "%(levelname)s:     %(asctime)s - %(message)s",
        },
        "default": {
            "format": "%(levelname)s:     %(asctime)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",  
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "filename": "../app.log",
        #     "formatter": "default",  
        # },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Apply logging configuration
dictConfig(LOGGING_CONFIG)

# Create logger
logger = logging.getLogger(__name__)
logger.info("Logger has been configured.")