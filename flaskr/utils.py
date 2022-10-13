import functools
from celery import Task
from importlib import import_module


def _wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_task(task):
    _task_module, task_name = task.split('.')
    task_module = import_module(f"tasks.{_task_module}")
    task = getattr(task_module, task_name)
    if not isinstance(task, Task): raise Exception(f"Invalid Task: {task}")
    return task
