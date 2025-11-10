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
    lab_id = db.Column (db.String(255), db.ForeignKey ("laboratoire.nomLab") )
    laboratoire = db.relationship ("Laboratoire", backref =db.backref ("plateformes", lazy="dynamic") )


    def __init__(self,nomPlateforme,nbPersonnes,cout,intervalleMaintenance,lieu):
        self.nomPlateforme= nomPlateforme
        self.nbPersonnes= nbPersonnes
        self.cout= cout
        self.intervalleMaintenance= intervalleMaintenance
        self.lieu= lieu

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
    
class Personne(db.Model):
    __tablename__ = 'personne'
    idP = db.Column( db.Integer, primary_key=True )
    nom = db.Column( db.String(255))
    prenom = db.Column(db.String(255))
    poste = db.Column( db.String(255))

    def __init__(self,nom,prenom,poste):
        self.nom= nom
        self.prenom= prenom
        self.poste= poste

    def __repr__(self):
        return "<%s %s (%i) au poste %s>" % (self.nom , self.prenom, self.idP, self.poste)
    

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