from flask import render_template, request
from flask import Blueprint
from logging import getLogger

from logger import logger_name
from flaskr.message import Message
from flaskr.utils import get_task, is_drop

tasker = Blueprint("tasker", __name__, url_prefix="/tasker")
logger = getLogger(logger_name)


@tasker.route("/api", methods=["GET", "POST"])
def api():
    if request.method == "GET": return "Get Method Is Not Allowed"
    data = Message(request).json()

    # is not drop, run action
    if not is_drop(data):
        action = data.get("action")
        action_name = action.get("name")
        action_kwargs = action.get("kwargs")

        try:
            task = get_task(action_name)
            result = task.delay(**action_kwargs)
        except TypeError as e:
            logger.warning(f"Error: {e}\nKwargs: {action_kwargs}")
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
        else:
            logger.info(f"Task: {action_name} [{result}] send")
            status = result.get() or ""
            if status == "ok":
                msg = f"Stat: {action_name} [{result}] {status}"
                logger.info(msg)
            else:
                msg = f"Stat: {action_name} [{result}] not ok\n{status}"
                logger.warning(msg)

    return render_template("base.html")
