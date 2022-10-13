from flask import render_template, request, Blueprint

from flaskr import logger
from flaskr.message import Message
from flaskr.utils import get_task

tasker = Blueprint("tasker", __name__, url_prefix="/tasker")


@tasker.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "GET": return "Get Method Is Not Allowed"
    msg = Message(request).json()

    action_name = msg.get("action")
    action_kwargs = msg.get("kwargs")

    try:
        task = get_task(action_name)
        result = task.delay(**action_kwargs)
    except TypeError as e:
        logger.warning(f"{e} kwargs: {action_kwargs}")
    except AttributeError as e:
        logger.warning(e)
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
    else:
        logger.info(
            '[ID [bold green]{}[/]] [bold green]"[/][bold medium_purple3]TASK[/] [green]/{}[/][bold green]"[/] send'.format(
                result, action_name
            ),
            extra={"markup": True, "highlighter": None},
        )

    return render_template("base.html")
