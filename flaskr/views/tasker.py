from flask import request, Blueprint

from flaskr import logger
from flaskr.message import Message
from flaskr.utils import get_task

tasker = Blueprint("tasker", __name__, url_prefix="/tasker")


@tasker.route("/ok", methods=["GET", "POST"])
def ok():
    return "ok"

@tasker.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "GET": return "Get Method Is Not Allowed"

    try:
        # construct message
        msg = Message(request).json()
        action_name = msg.get("action")
        action_kwargs = msg.get("kwargs")

        # run task
        task = get_task(action_name)
        result = task.delay(**action_kwargs)
    except Exception as e:
        logger.exception(e)
        return ""
    else:
        logger.info(
            '[ID [bold green]{}[/]] [bold green]"[/][bold medium_purple3]TASK[/] [green].{}[/][bold green]"[/] send'.format(
                result, action_name
            ),
            extra={"markup": True, "highlighter": None},
        )

    try:
        resp = result.get() or ""
    except Exception as e:
        logger.exception(e)
        return ""
    else:
        return resp

