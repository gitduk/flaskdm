from logging import getLogger
from flask import request, Blueprint

from flaskr.message import Message
from flaskr.utils import get_task

tasker = Blueprint("tasker", __name__, url_prefix="/tasker")
logger = getLogger(__name__)


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
        logger.info('[ID %s] "TASK .%s" send', result, action_name)

    try:
        resp = result.get() or ""
    except Exception as e:
        logger.exception(e)
        return ""
    else:
        return resp

