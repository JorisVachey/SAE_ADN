from .app import app,db
from flask import render_template, request, url_for , redirect, abort, jsonify, flash
from hashlib import sha256
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from .forms import LoginForm
from monApp.models import *
from monApp.forms import *
from sqlalchemy import desc,func
from datetime import date, datetime, timedelta
from werkzeug.utils import secure_filename
import random
import os
from functools import wraps
from monApp.utils import adn, fonctions_utiles, phylogenie

def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('connection'))
        # Vérifie le metier du user
        if not current_user.poste=="administration":
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def chercheur(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('connection'))
        # Vérifie le metier du user
        if not current_user.poste=="chercheur":
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def directeur(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('connection'))
        # Vérifie le metier du user
        if not current_user.poste=="directeur":
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def technicien(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si le user est connecté
        print(current_user)
        if not current_user.is_authenticated:
            flash("Veuillez vous connecter pour accéder à cette page.", "warning")
            return redirect(url_for('connection'))
        # Vérifie le metier du user
        if not current_user.poste=="technicien":
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

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
    return render_template('accueil.html', campagnes= infos_camp,plateformes=infos_plat, random=random)


@app.route('/plateforme/', methods=['GET','POST'])
@login_required
def create_plateforme():
    unForm = PlateformeForm()
    habForm = HabilitationForm()
    equipForm = EquipementForm()
    return render_template('ajout_plat.html', form = unForm, hab = habForm,equipements=equipForm)

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
    habForm = HabilitationForm()
    equipForm = EquipementForm()
    if unForm.validate_on_submit() and habForm.validate() and equipForm.validate():
        if unForm.Nom.data not in (p.nomPlateforme for p in Plateforme.query.filter(Plateforme.lab_id==lab.nomLab).all()):
            Nom = unForm.Nom.data
            nbPersonnes = unForm.nbPersonnes.data
            Cout = unForm.Cout.data
            IntervalleMaintenance = unForm.IntervalleMaintenance.data
            Lieu = unForm.Lieu.data
            plateforme = Plateforme(nomPlateforme =Nom,
                                    nbPersonnes=nbPersonnes,
                                    cout=Cout,
                                    intervalleMaintenance=IntervalleMaintenance,
                                    lieu=Lieu,
                                    derniereMaintenance=None,
                                    prochaineMaintenance=None
                                    )
            plateforme.laboratoire = lab
            db.session.add(plateforme)
            db.session.commit()
            habilitations = habForm.habilitation_selectionnee.data
            print(habilitations)
            for hab in habilitations :
                db.session.add(Necessite(type =hab,nomPlateforme=Nom))
                db.session.commit()

            equipements = equipForm.objets_selectionnes.data
            for eqp in equipements :
                db.session.add(Contenir(idE =eqp,nomPlateforme=Nom))
                db.session.commit()
            return redirect(url_for('accueil'))
        else:
            print("cette plateforme existe déjà")
    return render_template(
        'ajout_plat.html', 
        form = unForm, 
        hab = habForm, 
        equipements = equipForm
    )






@app.route('/campagne/', methods=['GET','POST'])
@login_required
def create_campagne():
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
    unForm = CampagneForm()
    return render_template('ajout_camp.html', form = unForm, plateformes=toutesPlat)


@app.route('/campagnes/ajouter-campagne/', methods=['GET','POST'])
@login_required
def ajouter_campagne():
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
    unForm = CampagneForm()
    if unForm.validate_on_submit():
            date = unForm.date.data
            duree = unForm.duree.data
            plat = request.form.get('plateforme')

            date_fin_nouv = date + timedelta(days=duree)
            
            date_fin_existante = db.func.datetime(Campagne.date, 
            Campagne.duree.cast(db.String) + db.literal(' days'))

            campagnes_existantes = Campagne.query.filter(Campagne.nomPlateforme == plat,Campagne.date < date_fin_nouv, date_fin_existante > date).all()
            campagne = Campagne(date=date,duree=duree, nomPlateforme=plat)
            if not campagnes_existantes:
                db.session.add(campagne)
                db.session.commit()
                return redirect(url_for('accueil'))
    return render_template('ajout_camp.html',form = unForm,plateformes=toutesPlat )

     




    
@app.route('/plateformes/<nomPlateforme>/', methods=['GET','POST'])
@login_required
def detail_plateforme(nomPlateforme):
    user = Personne.query.get_or_404(current_user.idP)
    unForm = PlateformeForm()
    try:
        participer = Participer.query.filter(Participer.idP == user.idP).one()
        camp = Campagne.query.filter(Campagne.numCampagne==participer.numCampagne).one()
        plat = Plateforme.query.filter(Plateforme.nomPlateforme==camp.nomPlateforme).one()
        lab=Laboratoire.query.filter(Laboratoire.nomLab==plat.lab_id).one()
        toutePlat = Plateforme.query.filter(Plateforme.lab_id==lab.nomLab).all()
        nomPlat = [p.nomPlateforme for p in toutePlat]
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
            print(unForm.ProchaineMaintenance.data)
            print( plat.derniereMaintenance)
            if (unForm.ProchaineMaintenance.data - datetime.strptime(plat.derniereMaintenance, '%Y-%m-%d').date()).days <= plat.intervalleMaintenance :
                plat.prochaineMaintenance = unForm.ProchaineMaintenance.data
                db.session.commit()
                infos["pro"]= plat.prochaineMaintenance
        return render_template('plateforme.html',plateforme = infos, objets=objets, maintenance=unForm, random=random)
    
    except Exception as e:
        print(f"Erreur lors de l'accès à la plateforme: {e}")
        return redirect(url_for('accueil'))
    

@app.route('/campagnes/<numCampagne>/')
@login_required
def detail_campagne(numCampagne):
    user = Personne.query.get_or_404(current_user.idP)
    camp = Campagne.query.filter(Campagne.numCampagne==numCampagne).one()
    try:
        """participer = Participer.query.filter(Participer.idP == user.idP, Participer.numCampagne==numCampagne).one()
        camp = Campagne.query.filter(Campagne.numCampagne==numCampagne).one()
        if not participer:
            return redirect(url_for('accueil'))"""

        if not user:
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
        return render_template('fouille.html',campagne = infos, personnes=personnes, random=random)
    except Exception as e:
        print(f"Erreur lors de l'accès à la plateforme: {e}")
        return redirect(url_for('accueil'))


@app.route('/echantillons/<int:numCampagne>/')
@login_required
def echantillons(numCampagne):
    campagne = Campagne.query.filter(Campagne.numCampagne==numCampagne).first_or_404()
    echantillons = Echantillon.query.filter(Echantillon.numCampagne==numCampagne).all()
    fichiers = [e.fichier for e in echantillons if e.fichier]
    all_file_details = {}
    
    for fichier in fichiers:

        echantillon = Echantillon.query.filter_by(idFichier=fichier.idFichier).first()
        
        if echantillon:
            all_file_details[str(fichier.idFichier)] = { 
                'idFichier': echantillon.idFichier,
                'idEchantillon': echantillon.numEchantillon,
                'espece': f"{echantillon.typeE} ({echantillon.nomSpecifique})",
                'commentaire': echantillon.commentaire
            }

    initial_details = {
        'idFichier': 'N/A', 
        'idEchantillon': 'N/A',
        'espece': 'Sélectionner un fichier',
        'commentaire': ''
    }
    if all_file_details:
        first_id = list(all_file_details.keys())[0]
        initial_details = all_file_details[first_id]

    return render_template('fichier_sequence.html', campagne=campagne,fichiers=fichiers, initial_details=initial_details,all_file_details=all_file_details, random=random)

@app.route('/echantillons/ajouter/<int:numCampagne>/', methods=['GET', 'POST'])
@login_required
def ajouter_echantillon(numCampagne):
    campagne = Campagne.query.get_or_404(numCampagne)
    form = EchantillonForm()
    fichier_form = FichierForm()

    if form.validate_on_submit() and fichier_form.validate_on_submit():
        f = fichier_form.nomFichier.data
        filename = secure_filename(f.filename)
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        filepath = os.path.join(upload_dir, filename)
        f.save(filepath)

        nouveau_fichier = Fichier(nomFichier=filename)
        db.session.add(nouveau_fichier)
        db.session.commit()

        echantillon = Echantillon(
            typeE=form.typeE.data,
            nomSpecifique=form.nomSpecifique.data,
            commentaire=form.commentaire.data,
            numCampagne=numCampagne,
            idP=current_user.idP
        )
        echantillon.idFichier = nouveau_fichier.idFichier
        db.session.add(echantillon)
        db.session.commit()

        return redirect(url_for('echantillons', numCampagne=numCampagne))

    return render_template('ajout_echantillon.html', form=form, fichier_form=fichier_form, campagne=campagne, random=random)


@app.route('/modif_plat/')
def modif_plat():
    unForm = PlateformeForm()
    habForm = HabilitationForm()
    equipForm = EquipementForm()
    return render_template('modif_plat.html', form = unForm, hab = habForm,equipements=equipForm)

@app.route('/modif_campagne/')
def modif_campagne():
    unForm = CampagneForm()
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
    return render_template('modif_campagne.html', form = unForm,plateformes=toutesPlat)
@app.route('/exploitation', methods=['GET'])
@login_required
def exploit():
    form_mutation = MutationForm()
    form_comparaison = ComparaisonForm()
    fichiers = Fichier.query.filter(Fichier.nomFichier.like('%.adn')).all()
    return render_template("exploitation.html", form_mutation=form_mutation, form_comparaison=form_comparaison, resultat_comparaison=None, fichiers=fichiers)

@app.route('/mutation', methods=['POST'])
@login_required
def mutation():
    form = MutationForm()
    if form.validate_on_submit():
        id_fichier = request.form.get('fichier_source')
        fichier = Fichier.query.get(id_fichier)
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        filepath = os.path.join(upload_dir, fichier.nomFichier)
        
        proba_r = form.proba_r.data / 100.0
        proba_d = form.proba_d.data / 100.0
        proba_i = form.proba_i.data / 100.0
        
        try:
            nouveau_chemin, modifs = adn.mutations(filepath, proba_r, proba_d, proba_i)
            nouveau_nom = os.path.basename(nouveau_chemin)
            
            # Enregistrement en BDD
            nouveau_fichier = Fichier(nomFichier=nouveau_nom)
            db.session.add(nouveau_fichier)
            db.session.commit()
            
            # Création d'un échantillon "virtuel" pour le voir dans la liste
            echantillon = Echantillon(
                typeE="Variant",
                nomSpecifique=f"Muté de {fichier.nomFichier}",
                commentaire=f"R:{form.proba_r.data}%, D:{form.proba_d.data}%, I:{form.proba_i.data}%",
                numCampagne=1, # Campagne par défaut ou à choisir
                idP=current_user.idP
            )
            echantillon.idFichier = nouveau_fichier.idFichier
            db.session.add(echantillon)
            db.session.commit()
            
            flash(f"Mutation réussie ! Fichier créé : {nouveau_nom}", "success")
            return redirect(url_for('exploit'))
        except Exception as e:
            print(f"Erreur mutation: {e}")
            flash(f"Erreur lors de la mutation : {e}", "error")
            return redirect(url_for('exploit'))
    else:
        flash("Formulaire invalide", "error")
    return redirect(url_for('exploit'))

@app.route('/comparaison', methods=['POST'])
@login_required
def comparaison():
    form = ComparaisonForm()
    resultat = None
    if form.validate_on_submit():
        id1 = request.form.get('fichier1')
        id2 = request.form.get('fichier2')
        f1 = Fichier.query.get(id1)
        f2 = Fichier.query.get(id2)
        
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        path1 = os.path.join(upload_dir, f1.nomFichier)
        path2 = os.path.join(upload_dir, f2.nomFichier)
        
        resultat = adn.distance_levenshtein(path1, path2)
            
    form_mutation = MutationForm()
    fichiers = Fichier.query.filter(Fichier.nomFichier.like('%.adn')).all()
    return render_template("exploitation.html", form_mutation=form_mutation, form_comparaison=form, resultat_comparaison=resultat, fichiers=fichiers)

@app.route('/phylogenie', methods=['POST'])
@login_required
def arbre_phylogenetique():
    # 1. Récupérer les fichiers
    fichiers_db = Fichier.query.filter(Fichier.nomFichier.like('%.adn')).all()
    upload_dir = os.path.join(app.root_path, 'static', 'uploads')
    
    especes = []
    # 2. Créer les objets EspeceAveree
    for f in fichiers_db:
        path = os.path.join(upload_dir, f.nomFichier)
        try:
            # On passe le chemin complet
            especes.append(phylogenie.EspeceAveree(path))
        except Exception as e:
            print(f"Erreur chargement {f.nomFichier}: {e}")

    if len(especes) < 2:
        flash("Il faut au moins 2 espèces pour construire un arbre.", "error")
        return redirect(url_for('exploit'))

    # 3. Reconstruire l'arbre
    try:
        racine = phylogenie.reconstruire_arbre_phylogenetique(especes)
        arbre_visuel = phylogenie.visualiser_arbre(racine)
    except Exception as e:
        flash(f"Erreur lors de la reconstruction : {e}", "error")
        return redirect(url_for('exploit'))
    
    # 4. Renvoyer le résultat à la page
    form_mutation = MutationForm()
    form_comparaison = ComparaisonForm()
    return render_template("exploitation.html", 
                         form_mutation=form_mutation, 
                         form_comparaison=form_comparaison, 
                         resultat_comparaison=None, 
                         fichiers=fichiers_db,
                         arbre_phylogenetique=arbre_visuel)