from flask_wtf import FlaskForm
from app.models import User
from wtforms import (
    StringField,
    DateField,
    SelectField,
    TelField,
    PasswordField,
    FormField,
    EmailField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Optional, Regexp, Email, EqualTo
from datetime import date


class PersonForm(FlaskForm):
    title = "Persona"

    name = StringField(label="Nombres", validators=[DataRequired(), Length(max=45)])
    parent_last = StringField(
        label="Apellido paterno", validators=[DataRequired(), Length(max=45)]
    )
    mother_last = StringField(
        label="Apellido materno", validators=[DataRequired(), Length(max=45)]
    )
    birthdate = DateField(label="Fecha de nacimiento", validators=[DataRequired()])
    curp = StringField(label="CURP", validators=[Length(max=18, min=18)])
    sex = SelectField(
        label="Sexo",
        coerce=bool,
        choices=[(True, "Masculino"), (False, "Femenino")],
        validators=[DataRequired()],
    )
    phone = TelField(
        label="Teléfono",
        validators=[
            Optional(),
            Length(max=12),
            Regexp(
                regex=r"^\d{3}-\d{3}-\d{4}$",
                message="El teléfono debe de tener el formato XXX-XXX-XXXX",
            ),
        ],
    )
    address = StringField(
        label="Dirección", validators=[DataRequired(), Length(max=256)]
    )
    email = EmailField(label="Email", validators=[DataRequired(), Email()])


class UserForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])


class RegisterUserForm(UserForm):
    title = "Usuario"
    confirm_password = PasswordField(
        label="Confirmar contraseña", validators=[DataRequired(), EqualTo("password")]
    )
    person = FormField(PersonForm)
    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("Ya existe un usuario con ese correo.")
