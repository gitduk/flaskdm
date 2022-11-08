import functools
import logging
from celery import Task
from importlib import import_module
from scrapyd_api import ScrapydAPI

logger = logging.getLogger(__name__)


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


def connect_to_scrapyd():
    try:
        scrapyd = ScrapydAPI('http://localhost:6800')
    except Exception as e:
        logger.exception(e)
    else:
        return scrapyd
