from flask_wtf import FlaskForm
from wtforms import FileField, SelectMultipleField, StringField, HiddenField, SelectField, IntegerField, RadioField, PasswordField, DateField
from wtforms.validators import DataRequired
from .models import *
from hashlib import sha256

class LoginForm(FlaskForm):
    Login = IntegerField('ID', validators=[DataRequired(message="Cette option est obligatoire")])
    Password = PasswordField('Mot de passe', validators=[DataRequired(message="Cette option est obligatoire")])
    next = HiddenField()

    def get_authenticated_user(self):
        unUser = Personne.query.filter_by(idP=self.Login.data).first()
        if unUser is None:
            return None
        m = sha256()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.mdp else None

class PlateformeForm(FlaskForm):
    Nom  = StringField('Nom plateforme', validators=[DataRequired(message="Cette option est obligatoire")])
    nbPersonnes = IntegerField('nb personnes', validators=[DataRequired(message="Cette option est obligatoire")])
    Cout = IntegerField('cout', validators=[DataRequired(message="Cette option est obligatoire")])
    IntervalleMaintenance  = IntegerField('nb jours entre maintenances', validators=[DataRequired(message="Cette option est obligatoire")])
    Lieu = StringField('lieu', validators=[DataRequired(message="Cette option est obligatoire")])
    ProchaineMaintenance = DateField('ProchaineMaintenance')

class HabilitationForm(FlaskForm):
    CHOICES = [
        ("Mobilier", "Mobilier"), ("Gros Électroménager", "Gros Électroménager"), 
        ("Petit Électroménager", "Petit Électroménager"), ("Service de Table", "Service de Table"), 
        ("Équipement audiovisuel", "Équipement audiovisuel"), ("Téléphonie", "Téléphonie"), 
        ("Décoration", "Décoration"), ("Linge", "Linge"), 
        ("Équipement informatique", "Équipement informatique"), ("Vêtements", "Vêtements"), 
        ("Provisions", "Provisions"), ("Materiel de bricolage", "Materiel de bricolage"), 
        ("Accessoires de loisirs", "Accessoires de loisirs"), ("Objets précieux", "Objets précieux"), 
        ("Divers", "Divers")
    ]
    habilitation_selectionnee = SelectMultipleField('Habilitations',choices=CHOICES, widget=CheckboxSelectMultiple() )
