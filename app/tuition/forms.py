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


class TuitionForm(FlaskForm):

    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=100)])
    price = DecimalField(
        label="Precio", validators=[DataRequired(), NumberRange(min=0.1)]
    )
    save = SubmitField("Guardar colegiatura")
