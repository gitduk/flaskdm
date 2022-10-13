from tasks.celery import celery

# load tasks
from tasks import local
from tasks import mail
from tasks import wechat
