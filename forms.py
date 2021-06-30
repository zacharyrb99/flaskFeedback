from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email
import email_validator

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('User email', validators=[InputRequired(), Email(message='Must input a valid email!')])
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Feedback', validators=[InputRequired()])