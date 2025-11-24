from .app import app,db
from flask import render_template, request, url_for , redirect, abort, jsonify
from hashlib import sha256
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from .forms import LoginForm
from monApp.models import *
from monApp.forms import *
from sqlalchemy import desc,func
from datetime import date, datetime


@app.route('/connexion/',methods=('GET','POST',))
def connexion():
    """
    Gère la connexion des utilisateurs.

    Si l'utilisateur est déjà connecté, il est redirigé vers le tableau de bord.
    Lors de la soumission du formulaire, tente d'authentifier l'utilisateur.
    En cas de succès, connecte l'utilisateur et le redirige.

    :returns: Redirection vers le tableau de bord (si déjà connecté ou après connexion réussie)
              ou le formulaire de connexion.
    """
    if current_user.is_authenticated:
        return redirect(url_for('accueil'))
    unForm = LoginForm ()
    unUser=None
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()
        if unUser:
            login_user(unUser)
            next = unForm.next.data or url_for("accueil")
            return redirect(next)
    return render_template('connexion.html',form=unForm)

@app.route('/deconnexion/')
def deconnexion():
    """
    Déconnecte l'utilisateur actuel.

    :returns: Redirection vers la page de connexion ('login').
    """
    logout_user()
    return redirect(url_for('connexion'))


@app.route('/')
@login_required
def accueil():
    pers = Personne.query.get_or_404(current_user.idP)
    participer = Participer.query.filter(Participer.idP == pers.idP).one()
    camp = Campagne.query.filter(
        Campagne.numCampagne == participer.numCampagne).one()
    lab = Laboratoire.query.filter(
        Laboratoire.nomLab == Plateforme.query.filter(
            Plateforme.nomPlateforme ==
            camp.nomPlateforme).one().lab_id).one()

    toutesPlat = Plateforme.query.filter(
        Plateforme.lab_id == lab.nomLab).order_by(
            Plateforme.nomPlateforme).all()
    infos_plat = list()
    for plat in toutesPlat:
        infos = dict()
        infos['nom'] = plat.nomPlateforme
        infos["maint"] = plat.derniereMaintenance
        infos["lieu"] = plat.lieu
        infos_plat.append(infos)

    nomsPlat = [plat.nomPlateforme for plat in toutesPlat]
    toutesCamp = Campagne.query.filter(Campagne.nomPlateforme.in_(nomsPlat)).all()

    infos_camp = list()
    for camp in toutesCamp:
        infos = dict()
        infos['num'] = camp.numCampagne
        infos["date"] = camp.date
        infos["duree"] = camp.duree
        infos["plat"]= camp.nomPlateforme
        infos_camp.append(infos)
    return render_template('accueil.html', campagnes= infos_camp,plateformes=infos_plat)

@app.route('/fouille/')
def fouille() :
    return render_template('fouille.html')



@app.route('/plateforme/', methods=['GET','POST'])
@login_required
def create_plateforme():
    unForm = PlateformeForm()
    return render_template('ajout_plat.html', formulaire = unForm)

@app.route('/plateformes/ajouter-plateforme/', methods=['GET','POST'])
@login_required
def ajouter_plateforme():
    pers = Personne.query.get_or_404(current_user.idP)
    participer = Participer.query.filter(Participer.idP == pers.idP).one()
    camp = Campagne.query.filter(
        Campagne.numCampagne == participer.numCampagne).one()
    lab = Laboratoire.query.filter(
        Laboratoire.nomLab == Plateforme.query.filter(
            Plateforme.nomPlateforme ==
            camp.nomPlateforme).one().lab_id).one()
    unForm = PlateformeForm()
    if unForm.validate_on_submit:
        Nom = unForm.Nom.data
        nbPersonnes = unForm.nbPersonnes.data
        Cout = unForm.Cout.data
        IntervalleMaintenance = unForm.IntervalleMaintenance.data
        Lieu = unForm.Lieu.data
        plateforme = Plateforme(nomPlateforme =Nom,
                                nbPersonnes=nbPersonnes,
                                cout=Cout,
                                intervalleMaintenance=IntervalleMaintenance,
                                lieu=Lieu
                                )
        plateforme.laboratoire = lab
        db.session.add(plateforme)
        db.session.commit()
        habilitations = request.form.getlist('habilitation')
        for hab in habilitations :
            db.session.add(Necessite(type =hab,nomPlateforme=Nom))
            db.session.commit()
        return redirect(url_for('accueil'))
    
@app.route('/plateformes/<nomPlateforme>/', methods=['GET','POST'])
@login_required
def detail_plateforme(nomPlateforme):
    user = Personne.query.get_or_404(current_user.idP)
    unForm = PlateformeForm()
    try:
        participer = Participer.query.filter(Participer.idP == user.idP).all()
        numParticip=[p.numCampagne for p in participer]
        campagnes = Campagne.query.filter(Campagne.numCampagne.in_(numParticip)).all()
        nomPlat=[c.nomPlateforme for c in campagnes]
        if not(nomPlateforme in nomPlat):
            return redirect(url_for('accueil'))

        plat = Plateforme.query.filter(Plateforme.nomPlateforme==nomPlateforme).one()
        infos = dict()
        infos['nom'] = plat.nomPlateforme
        infos["lieu"] = plat.lieu
        infos["pers"] = plat.nbPersonnes
        infos["intervalle"] = plat.intervalleMaintenance
        infos["maint"] = plat.derniereMaintenance
        infos["pro"]= plat.prochaineMaintenance
        infos["cout"] = plat.cout
        objets = []
        for obj in Contenir.query.filter(Contenir.nomPlateforme==nomPlateforme).all():
                objet = Equipement.query.filter(Equipement.idE==obj.idE).one()
                objets.append(objet)    
        if request.method == 'POST' and unForm.validate_on_submit:
            print(plat.prochaineMaintenance)
            print(unForm.ProchaineMaintenance.data)
            plat.prochaineMaintenance = unForm.ProchaineMaintenance.data
            db.session.commit()
            infos["pro"]= plat.prochaineMaintenance
            print(plat.prochaineMaintenance)
        return render_template('plateforme.html',plateforme = infos, objets=objets, maintenance=unForm)
    
    except Exception as e:
        print(f"Erreur lors de l'accès à la plateforme: {e}")
        return redirect(url_for('accueil'))
    

@app.route('/campagnes/<numCampagne>/')
@login_required
def detail_campagne(numCampagne):
    user = Personne.query.get_or_404(current_user.idP)
    try:
        participer = Participer.query.filter(Participer.idP == user.idP, Participer.numCampagne==numCampagne).one()
        camp = Campagne.query.filter(Campagne.numCampagne==numCampagne).one()
        if not participer:
            return redirect(url_for('accueil'))

        infos = dict()
        infos['numCampagne'] = camp.numCampagne
        infos["date"] = camp.date
        infos["duree"] = camp.duree
        infos["nomPlateforme"] = camp.nomPlateforme
        personnes = []
        for pers in Participer.query.filter(Participer.numCampagne==numCampagne).all():
                personne = Personne.query.filter(Personne.idP==pers.idP).one()
                personnes.append(personne)    
        return render_template('fouille.html',campagne = infos, personnes=personnes)
    except Exception as e:
        print(f"Erreur lors de l'accès à la plateforme: {e}")
        return redirect(url_for('accueil'))

@app.route('/campagnes/')
@login_required
def add_camp():
    return render_template('ajout_camp.html')