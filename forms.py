from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from models import User, Taco

def email_exists(form, field):
    """email_exists validator"""
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('Email already exists!')
    
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Login')
    
class TacoForm(Form):
    protein = StringField('Protein')
    shell = StringField('Shell')
    cheese = BooleanField('Cheese')
    extras = TextAreaField('Extras')
    submit = SubmitField('Add')
    
class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), email_exists])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2), EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm',)
    submit = SubmitField('Register')