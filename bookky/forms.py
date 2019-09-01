from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from bookky import db

class RegisterationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    agreement = BooleanField('Agreement');
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember_me');
    submit = SubmitField('Sign In')
