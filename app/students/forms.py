from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    SubmitField,
    DecimalField,
    IntegerField,
    TextAreaField,
    FormField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import schools_imgs
from app.forms import RegisterUserForm
from app.fields import GroupsField, TuitionField, ScholarshipsField


class StudentForm(FlaskForm):
    user = FormField(RegisterUserForm)
    group = GroupsField(
        label="Grupo",
        coerce=int,
        validators=[DataRequired()],
    )
    tuition = TuitionField(
        label="Colegiatura",
        coerce=int,
        validators=[DataRequired()],
    )
    scholarship = ScholarshipsField(
        label="Beca",
        coerce=int,
        validators=[],
    )
    save = SubmitField("Guardar alumno")
