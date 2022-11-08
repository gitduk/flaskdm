import os
import sys
import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler

from utils.log import ColorizedFormatter, DateFormat, Format

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

os.makedirs(LOG_DIR, exist_ok=True)


def init_logger():
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_formatter = ColorizedFormatter(fmt=Format.SIMPLE, datefmt=DateFormat.SIMPLE)
    stream_handler.setFormatter(stream_formatter)

    flask_file_handler = RotatingFileHandler(filename=LOG_DIR / "flask.log", maxBytes=5 * 1024 * 1024, backupCount=5)
    celery_file_handler = RotatingFileHandler(filename=LOG_DIR / "celery.log", maxBytes=5 * 1024 * 1024, backupCount=5)
    scrapy_file_handler = RotatingFileHandler(filename=LOG_DIR / "scrapy.log", maxBytes=5 * 1024 * 1024, backupCount=5)

    # root logger
    logging.basicConfig(level=logging.NOTSET, format=Format.SIMPLE, datefmt=DateFormat.SIMPLE,
                        handlers=[stream_handler])

    flask_logger = logging.getLogger(__name__)
    flask_logger.addHandler(stream_handler)
    flask_logger.addHandler(flask_file_handler)
    flask_logger.propagate = False

    celery_logger = logging.getLogger(__name__)
    celery_logger.setLevel(logging.INFO)
    celery_logger.addHandler(stream_handler)
    celery_logger.addHandler(celery_file_handler)
    celery_logger.propagate = False

    scrapy_logger = logging.getLogger(__name__)
    scrapy_logger.addHandler(stream_handler)
    scrapy_logger.addHandler(scrapy_file_handler)
    scrapy_logger.propagate = False
