from flask import render_template, request, Blueprint

from flaskr import logger
from flaskr.message import Message
from flaskr.utils import get_task, is_drop

tasker = Blueprint("tasker", __name__, url_prefix="/tasker")


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
            logger.info(f"[{result}] '{action_name}' send")
            status = result.get() or ""
            if status == "ok":
                msg = f"[{result}] '{action_name}' {status}"
                logger.info(msg)
            else:
                msg = f"[{result}] '{action_name}' not ok\n{status}"
                logger.warning(msg)

    return render_template("base.html")
