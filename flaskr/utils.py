import os
import functools
from celery import Task
from importlib import import_module
from dotenv import dotenv_values


def _wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def update_blacks(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        black_dotenv_path = os.path.join(os.path.abspath("."), ".env.black_list")
        os.environ.update(dotenv_values(black_dotenv_path))
        return func(*args, **kwargs)

    return wrapper


def get_task(task):
    _task_module, task_name = task.split('.')
    task_module = import_module(f"tasks.{_task_module}")
    task = getattr(task_module, task_name)
    if not isinstance(task, Task): raise Exception(f"Invalid Task: {task}")
    return task


@update_blacks
def is_drop(data):
    app = data.get("app")
    title = data.get("action", {}).get("kwargs", {}).get("title", "")

    black_app = os.getenv("BLACK_APP", [])
    black_title = os.getenv("BLACK_TITLE", [])

    if app in black_app or title in black_title:
        return True
    else:
        return False
