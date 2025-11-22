from datetime import datetime, date, timedelta
from enum import Enum
import enum
from .app import db
from flask_login import UserMixin
from sqlalchemy import Sequence

class Laboratoire(db.Model):
    __tablename__ = 'laboratoire'
    nomLab = db.Column( db.String(255), primary_key=True )
    adresse = db.Column( db.String(255))
    budget = db.Column( db.Integer)

    def __init__(self,nomLab,adresse,budget):
        self.nomLab= nomLab
        self.adresse= adresse
        self.budget= budget

    def __repr__(self):
        return "<Le laboratoire (%s) à l'adresse %s. Budget : %i>" % (self.nomLab , self.adresse, self.budget)
    

class Plateforme(db.Model):
    __tablename__ = 'plateforme'
    nomPlateforme = db.Column( db.String(255), primary_key=True )
    nbPersonnes = db.Column( db.Integer)
    cout = db.Column( db.Integer)
    intervalleMaintenance = db.Column( db.Integer)
    lieu = db.Column( db.String(255))
    derniereMaintenance = db.Column( db.String(10))
    prochaineMaintenance = db.Column(db.String(10))
    lab_id = db.Column (db.String(255), db.ForeignKey ("laboratoire.nomLab") )
    laboratoire = db.relationship ("Laboratoire", backref =db.backref ("plateformes", lazy="dynamic") )


    def __init__(self,nomPlateforme,nbPersonnes,cout,intervalleMaintenance,derniereMaintenance,prochaineMaintenance,lieu):
        self.nomPlateforme= nomPlateforme
        self.nbPersonnes= nbPersonnes
        self.cout= cout
        self.intervalleMaintenance= intervalleMaintenance
        self.lieu= lieu

        if derniereMaintenance is None:
            self.derniereMaintenance = date.today().strftime('%Y-%m-%d')
        else:
            self.derniereMaintenance = derniereMaintenance

        if prochaineMaintenance is None:
            try:
                dm_date = datetime.strptime(self.derniereMaintenance, '%Y-%m-%d')
                pm_date = dm_date + timedelta(days=intervalleMaintenance)
                self.prochaineMaintenance = pm_date.strftime('%Y-%m-%d')
            except ValueError:
                self.prochaineMaintenance = None 
        else:
            self.prochaineMaintenance = prochaineMaintenance

    def __repr__(self):
        return "<La plateforme (%s), %i personnes . intervalle : %i>" % (self.nomPlateforme , self.nbPersonnes, self.intervalleMaintenance)

class Equipement(db.Model):
    __tablename__ = 'equipement'
    idE = db.Column( db.Integer, primary_key=True )
    nomEquipement = db.Column( db.String(255))

    def __init__(self,nomEquipement):
        self.nomEquipement= nomEquipement

    def __repr__(self):
        return "<L'equipement numéro (%i), %s>" % (self.idE , self.nomEquipement)
    
class Contenir(db.Model):
    __tablename__ ='contenir'
    nomPlateforme = db.Column( db.String(255), db.ForeignKey ("plateforme.nomPlateforme"), primary_key =True)
    plateforme = db.relationship ("Plateforme", backref =db.backref ("contenus", lazy="dynamic") )
    idE = db.Column( db.Integer , db.ForeignKey ("equipement.idE"), primary_key =True)
    equipement = db.relationship ("Equipement", backref =db.backref ("contenus", lazy="dynamic") )  

    def __init__(self,nomPlateforme,idE):
        self.idE= idE
        self.nomPlateforme= nomPlateforme

    def __repr__(self):
        return "<La plateforme %s contient un equipement de ID : %i>" % (self.nomPlateforme , self.idE) 
    
class Campagne(db.Model):
    __tablename__ = 'campagne'
    numCampagne = db.Column( db.Integer, primary_key=True )
    date = db.Column( db.String(10))
    duree = db.Column(db.Integer)
    nomPlateforme = db.Column( db.String(255), db.ForeignKey ("plateforme.nomPlateforme"))
    plateforme = db.relationship ("Plateforme", backref =db.backref ("campagnes", lazy="dynamic") )

    def __init__(self,date,duree):
        self.date= date
        self.duree= duree

    def __repr__(self):
        return "<La campagne %i à partir du %s pendant %i jour(s) sur la plateforme %s>" % (self.numCampagne , self.date, self.duree, self.nomPlateforme)
    
class Personne(UserMixin,db.Model):
    __tablename__ = 'personne'
    idP = db.Column( db.Integer, primary_key=True )
    nom = db.Column( db.String(255))
    prenom = db.Column(db.String(255))
    poste = db.Column( db.String(255))
    mdp = db.Column(db.String(255))

    def __init__(self,nom,prenom,poste,mdp):
        self.nom= nom
        self.prenom= prenom
        self.poste= poste
        self.mdp=mdp

    def __repr__(self):
        return "<%s %s (%i) au poste %s>" % (self.nom , self.prenom, self.idP, self.poste)

    def get_id(self):
        return self.idP
    
from .app import login_manager
@login_manager.user_loader
def load_user(idP):
    return Personne.query.get(idP)
    

class Participer(db.Model):
    __tablename__ ='participer'
    numCampagne = db.Column( db.Integer, db.ForeignKey ("campagne.numCampagne"), primary_key =True)
    campagne = db.relationship ("Campagne", backref =db.backref ("participations", lazy="dynamic") )
    idP = db.Column( db.Integer , db.ForeignKey ("personne.idP"), primary_key =True)
    personne = db.relationship ("Personne", backref =db.backref ("participations", lazy="dynamic") )  

    def __init__(self,numCampagne,idP):
        self.idP= idP
        self.numCampagne= numCampagne

    def __repr__(self):
        return "<La personne (%i) participe à la campagne : %i>" % ( self.idP,self.numCampagne ) 
    
class Habilitation(db.Model):
    __tablename__ ='habilitation'
    type =  db.Column(db.Enum("Électrique", "Chimique", "Biologique", "Radiations", name="Type"), primary_key=True)

    def __init__(self,type):
        self.type= type

    def __repr__(self):
        return "<%s>" % ( self.type ) 
    

class Posseder(db.Model):
    __tablename__ ='posseder'
    type = db.Column( db.Integer, db.ForeignKey ("habilitation.type"), primary_key =True)
    habilitation = db.relationship ("Habilitation", backref =db.backref ("posseder", lazy="dynamic") )
    idP = db.Column( db.Integer , db.ForeignKey ("personne.idP"), primary_key =True)
    personne = db.relationship ("Personne", backref =db.backref ("posseder", lazy="dynamic") )  

    def __init__(self,type,idP):
        self.type= type
        self.idP= idP

    def __repr__(self):
        return "<La personne (%i) possede %s>" % ( self.idP,self.type ) 
    
class Necessite(db.Model):
    __tablename__ ='necessite'
    type = db.Column( db.Integer, db.ForeignKey ("habilitation.type"), primary_key =True)
    habilitation = db.relationship ("Habilitation", backref =db.backref ("necessite", lazy="dynamic") )
    nomPlateforme = db.Column( db.String(255), db.ForeignKey ("plateforme.nomPlateforme"), primary_key =True)
    plateforme = db.relationship ("Plateforme", backref =db.backref ("necessite", lazy="dynamic") )


    def __init__(self,type,nomPlateforme):
        self.type= type
        self.nomPlateforme= nomPlateforme

    def __repr__(self):
        return "<La plateforme (%s) à besoin de lhabilitation %s>" % ( self.nomPlateforme,self.type ) 

class Fichier(db.Model):
    __tablename__ = 'fichier'
    idFichier = db.Column( db.Integer, primary_key=True )
    nomFichier = db.Column(db.String(255))
    
    def __init__(self,nomFichier):
            self.nomFichier= nomFichier

    def __repr__(self):
            return "<le fichier %s (%i) >" % (self.nomFichier, self.idFichier)
    
class Echantillon(db.Model):
    __tablename__ = 'echantillon'
    numEchantillon = db.Column( db.Integer, primary_key=True )
    typeE = db.Column( db.String(255))
    nomSpecifique = db.Column(db.String(255))
    commentaire = db.Column( db.String(500))
    numCampagne = db.Column( db.Integer, db.ForeignKey ("campagne.numCampagne"))
    campagne = db.relationship ("Campagne", backref =db.backref ("echantillons", lazy="dynamic") )
    idP = db.Column( db.Integer , db.ForeignKey ("personne.idP"))
    personne = db.relationship ("Personne", backref =db.backref ("echantillons", lazy="dynamic") )  
    idFichier = db.Column (db.Integer, db.ForeignKey("fichier.idFichier"), nullable = True)
    fichier = db.relationship ("Fichier", backref =db.backref ("echantillons", lazy="dynamic") )  


    def __init__(self,typeE,nomSpecifique,commentaire,numCampagne,idP):
        self.typeE= typeE
        self.nomSpecifique= nomSpecifique
        self.commentaire= commentaire
        self.numCampagne= numCampagne
        self.idP= idP
        self.idFichier =None

    def __repr__(self):
        return "<l Echantillon (%i) de type %s, %s sur la campagne %i par la personne %i. ID Fichier :%i>" % (self.numEchantillon , self.typeE, self.nomSpecifique, self.numCampagne, self.idP, self.idFichier)
    
