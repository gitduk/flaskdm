from flask import render_template, request
from utils import create_app, get_data
import logging
from logger import logger_name
import json
import os
import requests

app = create_app()

logger = logging.getLogger(logger_name)
log = logging.getLogger("log")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("base.html")


@app.route("/sms", methods=["GET", "POST"])
def sms():
    if request.method == "GET": return "Get Method Is Not Allowed"
    data = get_data(request)
    logger.info(data)
    _from = data.get("from")
    body = data.get("body")
    date = data.get("date")
    _time = data.get("time")
    os.system(f"notify-send '{_from}' '{body} [{date} {_time}]'")
    return render_template("base.html")


@app.route("/sms/to/wechat", methods=["GET", "POST"])
def sms_to_wechat():
    if request.method == "GET": return "Get Method Is Not Allowed"

    data = get_data(request)
    logger.info(data)

    sms_from = data.get("from")
    sms_body = data.get("body")
    sms_send_date = data.get("date")
    sms_send_time = data.get("time")

    _id = data.get("id") or "ww30983d24fef1b8f4"
    secret = data.get("secret") or "bbVazDfYm5y6d5VlBw91mi205Oobyo5oywYLiszfTsg"
    agent_id = data.get("agentid") or "1000002"

    try:
        get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={_id}&corpsecret={secret}"
        resp = requests.get(get_token_url)
        token = resp.json().get("access_token")
    except:
        logger.warning("get token failed")
    else:
        # 转发到企业微信
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        content = f"{sms_body} \n\n时间: {sms_send_time} 日期: {sms_send_date}\n来自: {sms_from}"
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

    return render_template("base.html")


@app.route("/notify", methods=["GET", "POST"])
def notify():
    if request.method == "GET": return "Get Method Is Not Allowed"
    data = get_data(request)
    _app = data.get("app")
    title = data.get("title")
    content = data.get("content")
    log.info(data)
    if _app != "android":
        os.system(f"notify-send '{_app}: {title}' '{content}'")
    return render_template("base.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
