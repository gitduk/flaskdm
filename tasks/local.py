import os

from tasks.celery import celery
from tasks.utils import is_drop


@celery.task
def notify(app, title, content=""):
    # drop notify
    if is_drop(app, title): return f"drop {app}:{title}"

    if any([app, title, content]):
        os.system(f"notify-send '{app} - {title}' '{content}'")
    else:
        return "params is null"

    return "ok"
