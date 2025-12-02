from flask_wtf import FlaskForm
from wtforms import *
from wtforms import FileField, SelectMultipleField, StringField, HiddenField, SelectField, IntegerField, RadioField, PasswordField, DateField
from wtforms.validators import DataRequired
from .models import *
from hashlib import sha256
from wtforms.widgets.core import ListWidget, CheckboxInput

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
    ProchaineMaintenance = DateField('ProchaineMaintenance')

class HabilitationForm(FlaskForm):
    CHOICES = [
        ("Électrique", "Électrique"), ("Chimique", "Chimique"), 
        ("Biologique", "Biologique"), ("Radiations", "Radiations"), 
    ]
    habilitation_selectionnee = SelectMultipleField('Habilitations', 
            choices=CHOICES,
            widget=ListWidget(html_tag='ul', prefix_label=False),
            option_widget=CheckboxInput() 
        )
    
class FichierForm(FlaskForm):
    nomFichier = FileField('Fichier (.adn)', validators=[DataRequired(message="Cette option est obligatoire")])

class EchantillonForm(FlaskForm):
    typeE  = StringField('type espèce', validators=[DataRequired(message="Cette option est obligatoire")])
    nomSpecifique  = StringField('nom scientifique', validators=[DataRequired(message="Cette option est obligatoire")])
    commentaire = StringField('commentaire', validators=[DataRequired(message="Cette option est obligatoire")])

class EquipementForm(FlaskForm): # Renommé pour plus de clarté

    objets_selectionnes = SelectMultipleField(
        'Sélectionnez les Objets',
        widget=ListWidget(html_tag='ul', prefix_label=False),
        option_widget=CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        tous_les_objets = Equipement.query.all() 

        self.objets_selectionnes.choices = [
            (str(obj.idE), obj.nomEquipement) 
            for obj in tous_les_objets
        ]


class CampagneForm(FlaskForm):
    numCampagne = IntegerField('Numéro de la campgne')
    date  = DateField('date début', validators=[DataRequired(message="Cette option est obligatoire")])
    duree = IntegerField('nb jours', validators=[DataRequired(message="Cette option est obligatoire")])
    lieu = StringField('lieu',  validators=[DataRequired(message="Cette option est obligatoire")])

class MutationForm(FlaskForm):
    proba_r = IntegerField('Pourcentage Remplacement', default=0)
    proba_d = IntegerField('Pourcentage Délétion', default=0)
    proba_i = IntegerField('Pourcentage Insertion', default=0)

class ComparaisonForm(FlaskForm):
    methode = RadioField('Méthode', choices=[('levenshtein', 'Levenshtein')], default='levenshtein')

class LaboratoireForm(FlaskForm):
    nom=StringField('nom') 
    budget = IntegerField('budget', validators=[DataRequired(message="Cette option est obligatoire")])
