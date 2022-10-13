import os
import clipboard
import base64

from tasks.celery import celery, logger
from tasks.utils import is_drop


@celery.task
def notify(app, title, content=""):
    # drop notify
    if is_drop(app, title, content): return f"drop {app}:{title}:{content}"

    if any([app, title, content]):
        os.system(f"notify-send '{app} - {title}' '{content}'")
    else:
        return "params is null"

    return "ok"


@celery.task
def set_clipboard(text):
    clipboard.copy(text)
    return text or ""


@celery.task
def get_clipboard():
    return clipboard.paste() or ""


@celery.task
def share_file(file_name, file, save_path=None):
    save_path = save_path or os.path.join(os.getenv("HOME"), "Downloads")
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, file_name.split("/")[-1])

    try:
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(file))
    except Exception as e:
        logger.exception(e)
        logger.info(f"file: {file[:100]}")
        logger.info(f"file_name: {file_name}")

    return file_name
