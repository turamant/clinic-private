from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, Length, DataRequired, ValidationError


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


