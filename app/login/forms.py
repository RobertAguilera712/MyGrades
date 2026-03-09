from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    EmailField
)
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember me")
    submit = SubmitField(label="Log In")
