from importlib import import_module
from celery import Task

from flaskr.config import BLACK_APP, BLACK_TITLE


def get_task(task):
    _task_module, task_name = task.split('.')
    task_module = import_module(f"tasks.{_task_module}")
    task = getattr(task_module, task_name)
    if not isinstance(task, Task): raise Exception(f"Invalid Task: {task}")
    return task


def is_drop(data):
    app = data.get("app")
    title = data.get("action", {}).get("kwargs", {}).get("title", "")

    if app in BLACK_APP or title in BLACK_TITLE:
        return True
    else:
        return False
