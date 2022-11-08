import re

from tasks.celery import celery


def is_drop(app, title, content):
    black_app = celery.conf.get("BLACK_APP", [])
    black_title = celery.conf.get("BLACK_TITLE", [])
    black_content = celery.conf.get("BLACK_CONTENT", [])

    app_filter = [ba for ba in black_app if re.search(ba, app)] if app else []
    title_filter = [bt for bt in black_title if re.search(bt, title)] if title else []
    content_filter = [bc for bc in black_content if re.search(bc, content)] if content else []
    filter_list = [*app_filter, *title_filter, *content_filter]

    if not filter_list: return False

    return filter_list
