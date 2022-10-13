import json
import requests

from tasks.celery import celery


@celery.task
def send(_id, secret, agent_id, app="", title="", content=""):
    if not any([app, title, content]):
        return "data is null"

    try:
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={_id}&corpsecret={secret}"
        resp = requests.get(get_token_url)

        if resp.json().get("errcode") != 0:
            return "get token failed: {}".format(resp.json().get("errmsg"))

        token = resp.json().get("access_token")
    except Exception as e:
        return "get token failed: {}".format(e.__str__())
    else:
        # 转发到企业微信
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        content = f"{content}\n\n[{app}] {title}"
        request_body = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": agent_id,
            "text": {
                "content": content
            }
        }
        resp = requests.post(url, data=json.dumps(request_body))

        if resp.json().get("errcode") != 0:
            return "send data error: {}".format(resp.json().get("errmsg"))

        return "ok"
