import requests

from logging import getLogger
from flask import request, Blueprint, g, render_template, redirect, url_for

from flaskr.utils import connect_to_scrapyd

scrapyd = Blueprint("scrapyd", __name__, url_prefix="/scrapyd")
logger = getLogger(__name__)


@scrapyd.before_request
def set_scrapyd_api():
    if not g.get("scrapyd"):
        g.scrapyd = connect_to_scrapyd()


@scrapyd.route("/", methods=["GET", "POST"])
def root():
    return redirect(url_for("scrapyd.project", project="default")), 301


@scrapyd.route("/<project>", methods=["GET", "POST"])
def projects(project="default"):
    sd = g.get("scrapyd")
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 20))

    try:
        project_list = sd.list_projects()
        spider_list = [s for s in sd.list_spiders(project) if s]
        count_spider = len(spider_list)
        count_page = count_spider // page_size + 1
        spider_list = spider_list[(page - 1) * page_size:page * page_size]

    except requests.exceptions.ConnectionError:
        msg = "scrapyd not running"
    except Exception as e:
        logger.exception(e)

    return render_template("scrapyd/index.html", **locals())


@scrapyd.route("/<project>/<spider>", methods=["GET", "POST"])
def spiders(project, spider):
    pass
