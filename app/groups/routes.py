from flask import render_template, url_for, redirect, Blueprint, flash, request, session
from app.extensions import (
    bcrypt,
    role_required,
    db,
    users_imgs,
    compress_image,
)
from app.models import UserRole, Group, Person, User, Owner
from .forms import GroupForm
from flask_login import login_user, current_user, logout_user, login_required
from jinja2_fragments.flask import render_block
from .services import add_group, edit_group

groups = Blueprint(
    "groups",
    __name__,
    template_folder="../templates/groups",
    url_prefix="/groups",
)




@groups.get("/")
@login_required
@role_required([UserRole.OWNER])
def index():
    school_id = session.get("school_id")

    groups = Group.query.filter_by(school_id=school_id).all()
    template = "groups_index.jinja2"
    if "HX-Request" in request.headers:
        return render_block(template, "module", groups=groups)
    return render_template(template, groups=groups)

@groups.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def edit_form(id):
    form = GroupForm()
    group = Group.query.get(id)
    if form.save.data and form.validate_on_submit():
        if edit_group(form, group):
            flash("Grupo guardado con éxito", "success")
            return redirect(url_for("groups.index"))
        else:
            flash("Ocurrió un erro al guardar el grupo", "error")
    else:
        print(form.errors)

    template = "groups_form.jinja2"
    title = "Editar Grupo"
    form.name.data = group.name
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)



@groups.route("/add", methods=["GET", "POST"])
@login_required
@role_required([UserRole.OWNER])
def add_form():
    form = GroupForm()
    if form.save.data and form.validate_on_submit():
        school_id = session.get("school_id")
        if add_group(form, school_id):
            flash("Grupo guardado con éxito", "success")
            return redirect(url_for("groups.index"))
        else:
            flash("Ocurrió un erro al guardar el grupo", "error")
    else:
        print(form.errors)

    template = "groups_form.jinja2"
    title = "Agregar Grupo"
    if "HX-Request" in request.headers:
        return render_block(
            template, "module", title=title, form=form
        )
    return render_template(template, title=title, form=form)
