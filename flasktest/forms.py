from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo

from flask_login import current_user
from flasktest.models import User, Post

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                                validators= [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                                validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The Username is not available!")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("The email is not available!")


class UpdateUserAccount(FlaskForm):
    username = StringField('Username',
                                validators= [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                                validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The Username is not available!")

    def validate_email(self, email):
        if current_user.email != email.data:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("The email is not available!")



class LoginForm(FlaskForm):
    email = StringField('Email',
                                validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                                validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ResumePasswordForm(FlaskForm):
    email = StringField('Email',
                                validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')



