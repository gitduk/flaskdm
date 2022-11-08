import json

from logging import getLogger
from werkzeug.local import LocalProxy

logger = getLogger(__name__)


class Message(object):
    """
    construct message object from flask request
    """
    error_data = {
        "action": "local.notify",
        "kwargs": {
            "app": "flask",
            "title": "Warning",
            "content": ""
        }
    }

    def __init__(self, request=None, **kwargs):
        # parse request data
        if isinstance(request, LocalProxy):
            try:
                kwargs.update(self._get_data(request))
            except Exception as e:
                logger.exception(e)
                logger.warning(f"request.headers: {request.headers}")
                logger.warning(f"request.form: {request.form}")
                logger.warning(f"request.data: {request.data[:100]}")
                self.error_data["kwargs"]["content"] = "construct message failed"
                kwargs.update(self.error_data)

        self.action = kwargs.get("action", "")
        self.kwargs = kwargs.get("kwargs", {})

    def _get_data(self, request):
        content_type = request.headers.get("Content-Type", "").split(";")[0].strip()

        if content_type == "application/json":
            data = request.data
        elif content_type == "application/x-www-form-urlencoded":
            data = request.form
        elif content_type == "text/plain":
            data = request.data.decode("utf-8")
        else:
            self.error_data["kwargs"]["content"] = f"unsupported content type: {content_type}"
            data = self.error_data

        return data if isinstance(data, dict) else json.loads(data)

    def json(self):
        data = self.__dict__

        # 处理空值
        kwargs = data.get("kwargs")
        for k, v in kwargs.items():
            if isinstance(v, str) and v.startswith("%"):
                kwargs[k] = ""
        data["kwargs"] = kwargs

        return data

    def text(self):
        return json.dumps(self.json())

    def __str__(self):
        return json.dumps(self.__dict__)

    def __call__(self, **kwargs):
        return self.__dict__.update(**kwargs)
