from flask import render_template, url_for, redirect, Blueprint, flash, request
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import UserRole, School, Person, User
from .forms import SchoolForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .services import add_school

schools = Blueprint(
    "schools",
    __name__,
    template_folder="../templates/schools",
    url_prefix="/schools",
)


@schools.get("/")
@login_required
@role_required([UserRole.ADMIN])
def index():
    schools = School.query.all()
    template = "schools_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", schools=schools)
    return render_template(template, schools=schools)


@schools.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.ADMIN])
def add_form():
    form = SchoolForm()

    if form.save.data and form.validate_on_submit():
        if add_school(form):
            flash("Escuela guardada con éxito", "success")
            return redirect(url_for("schools.index"))
        else:
            flash("Ocurrió un erro al guardar la escuela", "error")
    else:
        print(form.errors)

    template = "schools_form.jinja2"
    title = "Agregar Escuela"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
