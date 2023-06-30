import logging
from os import getenv

from uvicorn.workers import UvicornWorker


class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        gunicorn_error_logger.handlers[0].setFormatter(
            logging.Formatter("[%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s")
        )
        uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
