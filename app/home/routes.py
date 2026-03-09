from flask import render_template, url_for, redirect, Blueprint, flash, request
from app.extensions import db
from jinja2_fragments.flask import render_block

home = Blueprint(
    "home", __name__, template_folder="../templates/home", url_prefix="/admin/home"
)


@home.route("/", methods=["GET"])
def index():
    template = "home.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module")
    return render_template(template,)
