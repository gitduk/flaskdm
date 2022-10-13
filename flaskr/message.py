import json
from werkzeug.local import LocalProxy


class Message(object):
    def __init__(self, request=None, **kwargs):
        if isinstance(request, LocalProxy):
            kwargs.update(self._get_data(request))

        self.action = kwargs.get("action", "notify")
        self.kwargs = kwargs.get("kwargs", {})

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
                    "action": "notify",
                    "kwargs": {}
                }
        else:
            data = json.loads(request.data.decode("utf-8"))

        return data

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
