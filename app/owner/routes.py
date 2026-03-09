from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.models import Owner
from app.extensions import db
from jinja2_fragments.flask import render_block
from flask_login import current_user


owner = Blueprint(
    "owner", __name__, template_folder="../templates/owner", url_prefix="/owner"
)


@owner.route("/", methods=["GET"])
def dashboard():
    template = "owner_dashboard.jinja2"
    owner = Owner.query.filter_by(user_id=current_user.id).first()
    session["owner_id"] = owner.id
    session["school_id"] = owner.school_id
    if "HX-Request" in request.headers:
        return render_block(template, "module")
    return render_template(template,)
