from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import UserRole, Student
from .forms import StudentForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .services import add_student

students = Blueprint(
    "students",
    __name__,
    template_folder="../templates/students",
    url_prefix="/students",
)




@students.get("/")
@login_required
@role_required([UserRole.OWNER])
def index():
    school_id = session.get("school_id")

    students = Student.query.filter_by(school_id=school_id).all()
    template = "students_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", students=students)
    return render_template(template, students=students)


@students.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def add_form():
    form = StudentForm()
    if form.save.data and form.validate_on_submit():
        school_id = session.get("school_id")
        if add_student(form, school_id):
            flash("Alumnos guardado con éxito", "success")
            return redirect(url_for("students.index"))
        else:
            flash("Ocurrió un erro al guardar el alumno", "error")
    else:
        print(form.errors)

    template = "students_form.jinja2"
    title = "Agregar Alumno"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
