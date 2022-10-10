import os
from celery import Celery
from logging import getLogger

from app import app
from logger import logger_name

logger = getLogger(logger_name)

# celery
if os.getenv('REDIS_PASSWORD'):
    CELERY_BROKER_URL = 'redis://:{}@localhost:6379/1'.format(os.getenv('REDIS_PASSWORD'))
    CELERY_RESULT_BACKEND = 'redis://:{}@localhost:6379/1'.format(os.getenv('REDIS_PASSWORD'))
else:
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

CELERYD_CONCURRENCY = 10  # 并发worker数量
CELERY_TIMEZONE = 'Asia/Shanghai'  # 时区
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ["json"]
CELERYD_ENABLE_UTC = True
CELERYD_FORCE_EXECV = True  # 防止死锁,应确保为True
CELERYD_PREFETCH_MULTIPLIER = 1  # 禁用任务预取
CELERYD_MAX_TASKS_PER_CHILD = 100  # worker执行100个任务自动销毁，防止内存泄露
CELERYD_TASK_SOFT_TIME_LIMIT = 6000  # 单个任务的运行时间不超过此值(秒)，否则会抛出(SoftTimeLimitExceeded)异常停止任务。
CELERY_DISABLE_RATE_LIMITS = True  # 即使任务设置了明确的速率限制，也禁用所有速率限制。

celery = Celery(
    app.import_name,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
