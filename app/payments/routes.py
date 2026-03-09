from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import Student, UserRole, Sell, Person, User, ScholarshipType
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .forms import PaymentForm

payments = Blueprint(
    "payments",
    __name__,
    template_folder="../templates/payments",
    url_prefix="/payments",
)


@payments.get("/")
@login_required
@role_required([UserRole.OWNER])
def index():
    school_id = session.get("school_id")
    payments = Sell.query.filter_by(school_id=school_id).all()
    template = "payments_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", payments=payments)
    return render_template(template, payments=payments)

@payments.get("get-details")
@login_required
@role_required([UserRole.OWNER])
def get_details():
    student_id = request.args.get("student")
    student = Student.query.get(student_id)
    return render_template("payment_info.jinja2", student=student, ScholarshipType=ScholarshipType )



@payments.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def add_form():
    form = PaymentForm()

    if form.save.data and form.validate_on_submit():
        school_id = session.get("school_id")
        # if add_scholarship(form, school_id):
        #     flash("Beca guardada con éxito", "success")
        #     return redirect(url_for("payments.index"))
        # else:
        #     flash("Ocurrió un erro al guardar la escuela", "error")
    else:
        print(form.errors)

    template = "payments_form.jinja2"
    title = "Cobrar"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
