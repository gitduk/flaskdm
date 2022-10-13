import os
import functools
from dotenv import dotenv_values


def update_blacks(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        dotenv_path = os.path.join(os.path.abspath("."), ".env")
        env_values = dotenv_values(dotenv_path)
        os.environ.setdefault("BLACK_APP", env_values.get("BLACK_APP"))
        os.environ.setdefault("BLACK_TITLE", env_values.get("BLACK_TITLE"))
        return func(*args, **kwargs)

    return wrapper


@update_blacks
def is_drop(app, title):
    black_app = os.getenv("BLACK_APP", [])
    black_title = os.getenv("BLACK_TITLE", [])

    if (app and app in black_app) or (title and title in black_title):
        return True
    else:
        return False
