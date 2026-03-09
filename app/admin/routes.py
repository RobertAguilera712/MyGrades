from flask import render_template, url_for, redirect, Blueprint, flash, request
from app.extensions import bcrypt
from .forms import LoginForm
from app.models import User, UserRole
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments import render_block

admin = Blueprint(
    "admin",
    __name__,
    template_folder="../templates/admin",
    url_prefix="/admin",
)

@admin.route("/", methods=["GET"])
def dashboard():
    template = "dashboard.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module")
    return render_template(template,)

