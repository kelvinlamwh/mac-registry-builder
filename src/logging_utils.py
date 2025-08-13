import logging
import inspect

from loguru import logger as loguru

LOGURU_ARGS = {
    'format': \
        "<green>{elapsed.seconds}.{elapsed.microseconds:06}</> | <level>{level: <8}</> | {name}:{function}:{line}\n"\
        "{message}\n",
    'colorize': None, # Auto-detection
}

class LoguruInterceptHandler(logging.Handler):
  def emit(self, record: logging.LogRecord) -> None:
    # Retrieve corresponding level in Loguru
    try:
        level = loguru.level(record.levelname).name
    except ValueError:
        level = record.levelno

    # Determine appropriate depth for Loguru
    depth = next(
       0 + depth
       for depth, frame in enumerate(inspect.stack())
       if frame.filename != logging.__file__ and depth > 0
    )
    loguru.opt(depth = depth, exception = record.exc_info).log(level, record.getMessage())

UVICORN_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'loguru': { 'class': LoguruInterceptHandler, },
    },
    'root': {
        'handlers': ['loguru'],
        'level': 0,
    },
    'loggers': {
        'uvicorn': { 'handlers': [ 'loguru' ], 'level': 'INFO', 'propagate': False },
        'uvicorn.error': { 'handlers': [ 'loguru' ], 'propagate': False },
        'uvicorn.access': { 'handlers': [ 'loguru' ], 'level': 'INFO', 'propagate': False },
    },
}
