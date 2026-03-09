from flask import render_template, url_for, redirect, Blueprint, flash, request
from app.extensions import bcrypt, role_required, db, services_imgs, get_current_time
from app.models import Service, UserRole
from .forms import ServiceForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block

services = Blueprint(
    "services",
    __name__,
    template_folder="../templates/services",
    url_prefix="/services",
)


@services.get("/")
@login_required
@role_required([UserRole.ADMIN])
def index():
    services = Service.query.all()
    if "HX-Request" in request.headers:
        return render_block("services_index.jinja2", "module", services=services)
    return render_template("services_index.jinja2", services=services)


@services.route("/agregar-servicio", methods=["GET", "POST"])
@login_required
@role_required([UserRole.ADMIN])
def add_form():
    form = ServiceForm()

    if form.save.data and form.validate_on_submit():
        try:
            service = Service()

            service.name = form.name.data
            service.description = form.description.data
            service.price = form.price.data
            service.slots = form.slots.data

            if form.image.data:
                image_name = f"{service.name}_{get_current_time().strftime("%Y-%m-%dT%H_%M_%S")}."
                image_filename = services_imgs.save(form.image.data, name=image_name)
                service.image_filename = image_filename

            db.session.add(service)
            db.session.commit()
            flash("Servicio guardado", "success")
            return redirect(url_for("services.index"))
        except Exception as ex:
            db.session.rollback()
            print(f"Ocurrió un error al guardar el servicio {str(ex)} {type(ex)}")
            flash("Error al guardar el servicio", "error")
    else:
        print(form.errors)

    if "HX-Request" in request.headers:
        return render_block(
            "services_form.jinja2", "module", title="Agregar servicio", form=form
        )
    return render_template("services_form.jinja2", title="Agregar servicio", form=form)
