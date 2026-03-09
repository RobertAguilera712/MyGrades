from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    SelectField,
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
from app.models import ScholarshipType


class SchoolarshipForm(FlaskForm):

    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=100)])
    discount = DecimalField(
        label="Descuento", validators=[DataRequired(), NumberRange(min=0.1)]
    )
    type = SelectField(
        label="Tipo",
        coerce= lambda value : ScholarshipType[value],
        choices=[(ScholarshipType.QUANTITY.name, "Cantidad"), (ScholarshipType.PERCENTAGE.name, "Porcentaje")],
        validators=[DataRequired()],
    )
    save = SubmitField("Guardar beca")
