from flask_wtf import FlaskForm
from wtforms import FileField, StringField, HiddenField, SelectField, IntegerField, RadioField, PasswordField, DateField
from wtforms.validators import DataRequired
from .models import *
from hashlib import sha256

class LoginForm(FlaskForm):
    Login = StringField ('ID')
    Password = PasswordField ('Mot de passe')
    next = HiddenField()

    def get_authenticated_user (self):
        unUser = Personne.query.filter_by(idP=self.Login.data).first()
        if unUser is None:
            return None
        m = sha256 ()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.mdp else None