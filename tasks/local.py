import os

from flaskr import logger
from tasks.celery import celery


@celery.task
def notify(**kwargs):
    app = kwargs.get('app')
    title = kwargs.get('title')
    content = kwargs.get('content')

    if not all([app, title, content]): logger.warning("invalid kwargs: {}".format(kwargs))

    os.system(f"notify-send '{app} - {title}' '{content}'")

    return "ok"
