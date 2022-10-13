import os
from pathlib import Path
from rich.console import Console

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

os.makedirs(LOG_DIR, exist_ok=True)

console = Console(width=120)

dict_config = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "{asctime} {levelname} {message}",
            "style": "{"
        },
        "verbose": {
            "format": "{asctime} {filename}:{lineno}:{funcName} [{levelname}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "rich": {
            "format": "{message}",
            "style": "{",
            "datefmt": "[%X]"
        },
    },
    "handlers": {
        "console": {
            "level": os.environ.get("LOG_LEVEL", "DEBUG"),
            # "class": "logging.StreamHandler",
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "console": console,
        },
        "flask_log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": LOG_DIR / "tasker.log",
            "mode": "w+",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 20,
            "encoding": "utf8",
        },
        "celery_log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "verbose",
            "filename": LOG_DIR / "celery.log",
            "mode": "w+",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 20,
            "encoding": "utf8",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "flask": {
            "handlers": ["console", "flask_log_file"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console", "celery_log_file"],
            "level": "INFO",
            "propagate": False,
        }
    },
}
