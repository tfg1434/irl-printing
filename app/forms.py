from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app import db
from app.models import User
import sqlalchemy as sa

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    username2 = StringField("Repeat Username", validators=[DataRequired(), EqualTo("username")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        if db.session.scalar(sa.select(User).where(User.username == username.data)) is not None:
            raise ValidationError("This username is already taken, please use a different one")
