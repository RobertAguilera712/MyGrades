from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import UserRole, Tuition, Person, User, Owner
from .forms import TuitionForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .services import add_tuition

tuition = Blueprint(
    "tuition",
    __name__,
    template_folder="../templates/tuition",
    url_prefix="/tuition",
)




@tuition.get("/")
@login_required
@role_required([UserRole.OWNER])
def index():
    school_id = session.get("school_id")

    tuitions = Tuition.query.filter_by(school_id=school_id).all()
    template = "tuition_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", tuitions=tuitions)
    return render_template(template, tuitions=tuitions)


@tuition.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def add_form():
    form = TuitionForm()
    if form.save.data and form.validate_on_submit():
        school_id = session.get("school_id")
        if add_tuition(form, school_id):
            flash("Colegiatura guardado con éxito", "success")
            return redirect(url_for("tuition.index"))
        else:
            flash("Ocurrió un erro al guardar la colegiatura", "error")
    else:
        print(form.errors)

    template = "tuition_form.jinja2"
    title = "Agregar Colegiatura"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
