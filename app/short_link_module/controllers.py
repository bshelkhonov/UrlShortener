from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)
from flask_login import login_required

from .models import Link
from .shorten_link import is_valid, add_to_db

short_link_module = Blueprint("short_link_module", __name__)


@short_link_module.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", result="")
    else:
        link = request.form["link"]
        if link == "":
            return redirect((url_for("shorten.index")))
        if not is_valid(link):
            return render_template("index.html", result="Invalid link")
        short_link = add_to_db(link)
        print(
            f"Link {link} was shortened to {short_link} and added to database")
        return render_template("index.html",
                               result=request.host + "/" + short_link)


@short_link_module.route("/history", methods=["GET"])
@login_required
def history():
    return render_template("history.html")


@short_link_module.route("/<short_link>")
def get_shorten_link(short_link):
    result = Link.query.filter(Link.short_link == short_link).all()
    if len(result) == 0:
        return redirect(url_for("shorten.index"))
    return redirect("http://" + result[0].original_link, code=302)

@short_link_module.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(
            url_for("users_module.login_page") + "?next=" + request.url)
    return response