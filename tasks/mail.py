import os
import smtplib
from email.mime.text import MIMEText

from tasks.celery import celery


@celery.task
def send(mail_to, subject="", content=""):
    server = os.getenv("MAIL_SERVER")
    sender = os.getenv("MAIL_SENDER")
    password = os.getenv("MAIL_PASSWORD")
    try:
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = mail_to

        smtp = smtplib.SMTP_SSL(server)
        smtp.login(sender, password)
        smtp.sendmail(sender, mail_to, msg.as_string())
        smtp.quit()
    except Exception as e:
        return e.__str__()
    else:
        return "ok"
