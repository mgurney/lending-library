"""Signup & login forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Signup Form."""
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[Length(min=6), Email(message='Enter a valid email.'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    read_rules = BooleanField('Have you read the Rules', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class AddDvdForm(FlaskForm):
    """ Form to add DVD to the database ready for lending"""
    title = StringField('Title', validators=[DataRequired(), Length(max=50, message='Only 50 characters allowed')])
    format_dvd = BooleanField('DVD?', validators=[Optional()])
    format_bluray = BooleanField('Blu-Ray?', validators=[Optional()])
    format_4k = BooleanField('4K?', validators=[Optional()])
    rating = SelectField('Rating', choices=[('U', 'U'), ('PG','PG'), ('12', '12'), ('12A', '12A'), ('15', '15'), ('18', '18')])
    submit = SubmitField('Submit')

class AddMagForm(FlaskForm):
    """ Form to add Magazine to the database ready for lending"""
    title = StringField('Title', validators=[DataRequired(), Length(max=50, message='Only 50 characters allowed')])
    submit = SubmitField('Submit')