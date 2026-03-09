from flask import render_template, url_for, redirect, Blueprint, flash, request
from app.extensions import bcrypt
from .forms import LoginForm
from app.models import User, UserRole
from flask_login import login_user, current_user, logout_user, login_required

login = Blueprint(
    "login",
    __name__,
    template_folder="../templates/login",
    url_prefix="/login",
)

default_routes = {
    UserRole.ADMIN: "admin.dashboard",
    UserRole.OWNER: "owner.dashboard",
    UserRole.EMPLOYEE: "employee.dashboard",
}


@login.route("/", methods=["GET", "POST"])
def log_in():
    if current_user.is_authenticated:
        default_page = default_routes.get(current_user.role, "login.login")
        return redirect(url_for(default_page))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                default_page = default_routes.get(user.role, "login.log_in")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for(default_page))
                )
            else:
                flash(f"El usuario o la contraseña son incorrectos", "danger")
        else:
            flash(f"El usuario o la contraseña son incorrectos", "danger")
    return render_template("login.jinja2", title="login", form=form)

@login.route("/out")
@login_required
def logout():
    logout_user()
    return redirect(url_for("page.home"))
