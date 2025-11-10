from flask_wtf import FlaskForm
from wtforms import FileField, StringField, HiddenField, SelectField, IntegerField, RadioField, PasswordField, DateField
from wtforms.validators import DataRequired
from .models import *
from hashlib import sha256

