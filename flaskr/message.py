import json
from werkzeug.local import LocalProxy
from datetime import datetime
from logging import getLogger

from logger import logger_name

logger = getLogger(logger_name)


class Message(object):
    def __init__(self, request=None, **kwargs):
        if isinstance(request, LocalProxy):
            kwargs.update(self._get_data(request))

        self.app = kwargs.get("app")
        self.time = kwargs.get("time")
        self.action = kwargs.get("action")

    @staticmethod
    def _get_data(request):
        content_type = request.headers.get("Content-Type", "")
        if content_type.startswith("application"):
            if content_type == "application/json":
                data = request.data
            elif content_type == "application/x-www-form-urlencoded":
                data = request.form
            else:
                data = {
                    "app": "flaskr",
                    "time": str(datetime.now()),
                    "action": {
                        "name": "notify",
                        "kwargs": {}
                    }
                }
        else:
            data = json.loads(request.data.decode("utf-8"))

        return data

    def json(self):
        # 处理空值
        data = self.__dict__
        for k, v in data.items():
            if not isinstance(v, str): continue
            if not v or v.startswith("%"): data[k] = ""

        action = data.get("action")
        if not action:
            logger.warning(f"invalid action: {action}")
        else:
            for k, v in action.items():
                if not isinstance(v, str): continue
                if not v or v.startswith("%"): action[k] = ""
            data["action"] = action

        return data

    def text(self):
        return json.dumps(self.json())

    def __str__(self):
        return json.dumps(self.__dict__)

    def __call__(self, **kwargs):
        return self.__dict__.update(**kwargs)
