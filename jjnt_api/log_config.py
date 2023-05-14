from logging import getLogger
from logging.config import dictConfig

from pydantic import BaseModel


class _LogConfig(BaseModel):
    """
    Logging configuration to be set for the server
    """

    LOGGER_NAME: str = "jjnt-logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


# Logger
_log_config = _LogConfig()
dictConfig(_log_config.dict())
logger = getLogger(_log_config.LOGGER_NAME)
