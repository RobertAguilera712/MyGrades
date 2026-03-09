from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import UserRole, Scholarship, Person, User, ScholarshipType
from .forms import SchoolarshipForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .services import add_scholarship

scholarships = Blueprint(
    "scholarships",
    __name__,
    template_folder="../templates/scholarships",
    url_prefix="/scholarships",
)


@scholarships.get("/")
@login_required
@role_required([UserRole.OWNER])
def index():
    school_id = session.get("school_id")
    scholarships = Scholarship.query.filter_by(school_id=school_id).all()
    template = "scholarships_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", scholarships=scholarships, ScholarshipType=ScholarshipType)
    return render_template(template, scholarships=scholarships, ScholarshipType=ScholarshipType)


@scholarships.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def add_form():
    form = SchoolarshipForm()

    if form.save.data and form.validate_on_submit():
        school_id = session.get("school_id")
        if add_scholarship(form, school_id):
            flash("Beca guardada con éxito", "success")
            return redirect(url_for("scholarships.index"))
        else:
            flash("Ocurrió un erro al guardar la escuela", "error")
    else:
        print(form.errors)

    template = "scholarships_form.jinja2"
    title = "Agregar Beca"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
