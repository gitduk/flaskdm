import json
import requests

from tasks.celery import celery, logger


@celery.task
def send(**kwargs):
    _id = kwargs.get("id")
    secret = kwargs.get("secret")
    agent_id = kwargs.get("agent_id")
    app = kwargs.get("app")
    title = kwargs.get("title")
    content = kwargs.get("content")

    try:
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={_id}&corpsecret={secret}"
        resp = requests.get(get_token_url)
        token = resp.json().get("access_token")
    except:
        logger.warning("get token failed")
    else:
        # 转发到企业微信
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        content = f"app: {app}\ntitle:{title}\ncontent:{content}"
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
            errmsg = resp.json().get("errmsg")
            logger.warning(f"发送失败: {errmsg}")

    return "ok"
