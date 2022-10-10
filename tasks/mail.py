import os
from flask_mail import Message

from app import mail, app
from tasks.celery import celery


@celery.task
def send(mail_to, subject="", content="", html=""):
    try:
        msg = Message(
            subject=subject,
            sender=os.getenv("MAIL_USERNAME"),
            recipients=[mail_to]
        )
        msg.body = content
        msg.html = html

        with app.app_context():
            mail.send(msg)
    except Exception as e:
        return e.__str__()

    return "ok"
