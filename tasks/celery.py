import os
import logging
from celery import Celery
from celery.signals import setup_logging
from logging.config import dictConfig

from logger import dict_config
from flaskr.app import app
from tasks.config import CONFIGS

# create and config celery
celery = Celery(app.import_name)
config_name = os.getenv("CELERY_CONFIG", "default")
celery.config_from_object(CONFIGS[config_name])


@setup_logging.connect
def logger_setup_handler(*args, **kwargs):
    dictConfig(dict_config)


# celery logging configuration
logger = logging.getLogger("celery")
