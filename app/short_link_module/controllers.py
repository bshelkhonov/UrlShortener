from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)

from .models import Link
from .shorten_link import is_valid, add_to_db, add_prefix
from app.database import db

short_link_module = Blueprint("short_link_module", __name__)


@short_link_module.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        result = ""
        if "result" in request.args:
            result = request.args.get("result")
        return render_template("index.html", result=result)
    else:
        link = request.form["link"]
        if link == "":
            return redirect((url_for("short_link_module.index")))
        link = add_prefix(link)
        if not is_valid(link):
            return render_template("index.html", result="Invalid link")
        short_link = add_to_db(link)
        print(
            f"Link {link} was shortened to {short_link} and added to database")

        short_link = request.host + "/" + short_link

        return redirect(
            url_for("short_link_module.index") + "?result=" + short_link)


@short_link_module.route("/<short_link>")
def get_shorten_link(short_link):
    result = Link.query.filter(Link.short_link == short_link).first()
    if not result:
        return redirect(url_for("short_link_module.index"))

    result.usages_num += 1
    db.session.commit()
    original_link = result.original_link

    return redirect(original_link, code=302)


@short_link_module.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(
            url_for("users_module.login_page") + "?next=" + request.url)
    return response
