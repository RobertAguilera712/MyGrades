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
from app.fields import StudentsField


class PaymentForm(FlaskForm):
    student = StudentsField(label="Alumno", validators=[DataRequired()])
    save = SubmitField("Cobrar")
