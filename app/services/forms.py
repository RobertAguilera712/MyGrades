from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    DecimalField,
    IntegerField,
    TextAreaField
)
from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange,
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import services_imgs


class ServiceForm(FlaskForm):
    title = "Servicio"

    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField(label="Descripción", validators=[DataRequired()])
    image = FileField(validators=[FileAllowed(services_imgs, "Image only")])
    price = DecimalField(
        label="Precio", validators=[DataRequired(), NumberRange(min=0.1)]
    )
    slots = IntegerField(label="Slots", validators=[DataRequired(), NumberRange(min=1)], default=1)
    save = SubmitField("Guardar servicio")
