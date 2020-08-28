from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email,ValidationError
from wtforms.fields.html5 import EmailField

from email_validator import validate_email
from flaskBlog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2,max=20)])
    email = StringField('Email',validators = [DataRequired(), Length(min=2,max=40),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = EmailField('Email',validators = [DataRequired(), Length(min=2,max=40)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
