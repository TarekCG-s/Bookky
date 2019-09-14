from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, Email
from bookky import db

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    agreement = BooleanField("I've read the website terms and I agree to follow them", validators=[DataRequired()]);
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember_me');
    submit = SubmitField('Sign In')

class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class UpdatePicture(FlaskForm):

    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upload Photo')
