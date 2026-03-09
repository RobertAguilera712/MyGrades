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


class SchoolForm(FlaskForm):
    title = "Escuela"

    image = FileField(validators=[FileAllowed(schools_imgs, "Image only")])
    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=100)])
    address = StringField(
        label="Dirección", validators=[DataRequired(), Length(max=256)]
    )
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    owner = FormField(RegisterUserForm)
    save = SubmitField("Guardar escuela")
