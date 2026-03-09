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


## ADD THE POSSIBILITY TO ADD STUDENTS DIRECTLY FROM HERE
class GroupForm(FlaskForm):

    name = StringField(label="Nombre", validators=[DataRequired(), Length(max=100)])
    save = SubmitField("Guardar grupo")
