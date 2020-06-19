# blueprint for user only forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    # requirement user name to be not empty using datarequired validator, make sure username between 2 to 20 character using length validator
    email = StringField('Email',validators=[DataRequired(), Email()]) #make sure email is valid email using email validator
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) #make sure confirm password is equal to password

    submit = SubmitField('Sign Up') # finish registration

    # if registration username already exists, raise error
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    # if registration email already exists, raise error
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    # requirement user name to be not empty using datarequired validator, make sure username between 2 to 20 character using length validator
    email = StringField('Email',
                        validators=[DataRequired(), Email()])  # make sure email is valid email using email validator
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') # remember to be logged in

    submit = SubmitField('Login')  # finish log in


# For user to update account information after logged

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    # requirement user name to be not empty using datarequired validator, make sure username between 2 to 20 character using length validator
    email = StringField('Email',validators=[DataRequired(), Email()]) #make sure email is valid email using email validator

    # create change profile picture field, and only allow jpg and png file submission
    picture =FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update') # finish registration

    # if registration username already exists, raise error
    def validate_username(self, username):
        # only check if the username they entered is different from user's current name
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    # if registration email already exists, raise error
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


# create form for request reset form
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Request Passwork Reset')

    # if registration email not exists, raise error, let user know they need to create account first
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

# create form to reset password
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) #make sure confirm password is equal to password
    submit = SubmitField('Reset Passwork')