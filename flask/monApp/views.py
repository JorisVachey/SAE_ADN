from .app import app,db
from flask import render_template, request, url_for , redirect, abort, jsonify
from hashlib import sha256
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from .forms import LoginForm
from monApp.models import *
from monApp.forms import *
from sqlalchemy import desc,func
from datetime import date, datetime
import random



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
    unUser=Nfirst
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
    participer = Participer.query.filter(Participer.idP == pers.idP).first()
    camp = Campagne.query.filter(
        Campagne.numCampagne == participer.numCampagne).first()
    lab = Laboratoire.query.filter(
        Laboratoire.nomLab == Plateforme.query.filter(
            Plateforme.nomPlateforme ==
            camp.nomPlateforme).first().lab_id).first()

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
    participer = Participer.query.filter(Participer.idP == pers.idP).first()
    camp = Campagne.query.filter(
        Campagne.numCampagne == participer.numCampagne).first()
    lab = Laboratoire.query.filter(
        Laboratoire.nomLab == Plateforme.query.filter(
            Plateforme.nomPlateforme ==
            camp.nomPlateforme).first().lab_id).first()
    
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
                                    derniereMaintenance=Nfirst,
                                    prochaineMaintenance=Nfirst
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




def get_date_fin(date_debut_str, duree_jours):
    """Calcule la date de fin d'une campagne."""
    try:
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        return date_debut + timedelta(days=int(duree_jours))
    except (ValueError, TypeError):
        return Nfirst

def check_personne_qualification(personne_id, nomPlateforme):
    """Vérifie si la personne possède toutes les habilitations nécessaires pour la plateforme."""
    
    # Utilisation des classes de modèle (SQLAlchemy)
    required_types = [n.type for n in Necessite.query.filter_by(nomPlateforme=nomPlateforme).all()]
    
    if not required_types:
        return True
        
    possessed_types = [p.type for p in Posseder.query.filter_by(idP=personne_id).all()]
    
    # La personne doit posséder TOUTES les habilitations requises
    for req_type in required_types:
        if req_type not in possessed_types:
            return False 
    
    return True

def get_personnes_du_laboratoire_de_la_campagne_actuelle():
    pers_connectee = Personne.query.get_or_404(current_user.idP)

    participation = Participer.query.filter(Participer.idP == pers_connectee.idP).first()

    if not participation:
        return []

    campagne_actuelle = Campagne.query.get_or_404(participation.numCampagne)
    
    plat_source = Plateforme.query.filter(Plateforme.nomPlateforme == campagne_actuelle.nomPlateforme).first()
    
    nom_laboratoire = plat_source.lab_id
    
    # 1. Sous-requête : Toutes les plateformes du laboratoire
    plateformes_du_labo = Plateforme.query.filter(
        Plateforme.lab_id == nom_laboratoire
    ).subquery()
    
    # 2. Sous-requête : Toutes les campagnes sur ces plateformes
    campagnes_du_labo = Campagne.query.filter(
        Campagne.nomPlateforme.in_(db.session.query(plateformes_du_labo.c.nomPlateforme))
    ).subquery()
    
    # 3. Requête finale : Toutes les personnes participant à ces campagnes
    personnes_du_labo = db.session.query(Personne).join(Participer).filter(
        Participer.numCampagne.in_(db.session.query(campagnes_du_labo.c.numCampagne))
    ).order_by(Personne.nom).all()

    return personnes_du_labo

def get_personnes_disponibles(nomPlateforme, date_debut_str, duree_jours):
    """
    Trouve les personnes qui sont qualifiées (habilitations) et disponibles (pas de chevauchement).
    """
    
    if not date_debut_str or not duree_jours or int(duree_jours) <= 0:
        return []
        
    date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
    date_fin = get_date_fin(date_debut_str, duree_jours)

    if not date_fin:
        return []

    personnes_disponibles = []
    toutes_les_personnes = get_personnes_du_laboratoire_de_la_campagne_actuelle()
    
    for personne in toutes_les_personnes:
        personne_id = personne.idP
        
        # 1. Vérification des Habilitations (Qualification)
        if not check_personne_qualification(personne_id, nomPlateforme):
            continue
            
        # 2. Vérification des Conflits de Planning
        participations_existantes = Participer.query.filter_by(idP=personne_id).all()
        
        conflit_trouve = False
        for participation in participations_existantes:
            campagne_existante = Campagne.query.get(participation.numCampagne)
            
            if campagne_existante:
                try:
                    date_debut_existante = datetime.strptime(campagne_existante.date, '%Y-%m-%d').date()
                    date_fin_existante = get_date_fin(campagne_existante.date, campagne_existante.duree)
                except (ValueError, TypeError):
                    continue

                if (date_debut < date_fin_existante) and (date_fin > date_debut_existante):
                    conflit_trouve = True
                    break
        
        if not conflit_trouve:
            personnes_disponibles.append(personne)
                
    return personnes_disponibles

# --- Route API JSON (Cible du JavaScript) ---

@app.route('/api/get_disponibilites', methods=['POST'])
def api_get_disponibilites():
    """Route API qui reçoit les paramètres et retourne la liste des personnes disponibles en JSON."""
    
    if not request.is_json:
        return jsonify({'error': 'Le contenu doit être de type JSON'}), 415
        
    data = request.get_json()
    
    nomPlateforme = data.get('plateforme')
    date_debut = data.get('date')
    duree = data.get('duree')
    
    if not all([nomPlateforme, date_debut, duree]) or not str(duree).isdigit() or int(duree) <= 0:
        return jsonify({'error': 'Paramètres (plateforme, date, durée) manquants ou invalides'}), 400

    try:
        personnes = get_personnes_disponibles(nomPlateforme, date_debut, duree)
        
        # Format attendu par le JavaScript : [{id: 1, nom_complet: "Prenom Nom (Poste)"}, ...]
        resultat = []
        for p in personnes:
            resultat.append({
                'id': p.idP,
                'nom_complet': f"{p.prenom} {p.nom} ({p.poste})"
            })
            
        return jsonify({'personnes': resultat})
        
    except Exception as e:
        print(f"Erreur lors de la recherche de disponibilité : {e}")
        return jsonify({'error': 'Erreur interne du serveur lors du traitement des données.'}), 500


# --- Routes de l'Application (Gestion de la vue) ---

@app.route('/campagne/', methods=['GET','POST'])
@login_required
def create_campagne():
    # Logique pour charger les plateformes (inchangée)
    try:
        pers = Personne.query.get_or_404(current_user.idP)
        participer = Participer.query.filter(Participer.idP == pers.idP).first()
        camp = Campagne.query.filter(Campagne.numCampagne == participer.numCampagne).first()
        plat_source = Plateforme.query.filter(Plateforme.nomPlateforme == camp.nomPlateforme).first()
        lab = Laboratoire.query.filter(Laboratoire.nomLab == plat_source.lab_id).first()
        toutesPlat = Plateforme.query.filter(
            Plateforme.lab_id == lab.nomLab).order_by(Plateforme.nomPlateforme).all()
    except:
        toutesPlat = Plateforme.query.order_by(Plateforme.nomPlateforme).all()
        
    unForm = CampagneForm()
    return render_template('ajout_camp.html', form = unForm, plateformes=toutesPlat)


@app.route('/campagnes/ajouter-campagne/', methods=['POST'])
@login_required
def ajouter_campagne():
    unForm = CampagneForm()
    
    # Logique pour le rechargement en cas d'erreur
    try:
        pers = Personne.query.get_or_404(current_user.idP)
        participer = Participer.query.filter(Participer.idP == pers.idP).first()
        camp = Campagne.query.filter(Campagne.numCampagne == participer.numCampagne).first()
        plat_source = Plateforme.query.filter(Plateforme.nomPlateforme == camp.nomPlateforme).first()
        lab = Laboratoire.query.filter(Laboratoire.nomLab == plat_source.lab_id).first()
        toutesPlat = Plateforme.query.filter(
            Plateforme.lab_id == lab.nomLab).order_by(Plateforme.nomPlateforme).all()
    except:
        toutesPlat = Plateforme.query.order_by(Plateforme.nomPlateforme).all()
    
    if unForm.validate_on_submit():
        date_campagne = unForm.date.data
        duree = unForm.duree.data
        nomPlateforme = request.form.get('plateforme')
        
        # Récupération des IDs des personnes cochées
        personnes_ids = request.form.getlist('personnes_choisies') 
        print(personnes_ids)

        date_fin_nouv = date_campagne + timedelta(days=duree)
        
        # Vérification de la disponibilité de la PLATEFORME 
        date_fin_existante = db.func.datetime(Campagne.date, 
        Campagne.duree.cast(db.String) + db.literal(' days'))

        campagnes_existantes_sur_plat = Campagne.query.filter(
            Campagne.nomPlateforme == nomPlateforme,
            Campagne.date < date_fin_nouv, 
            date_fin_existante > date_campagne
        ).all()
        
        # Vérification des personnes sélectionnées 
        if not personnes_ids:
            # flash("Veuillez sélectionner au moins une personne participante.", 'danger')
            return render_template('ajout_camp.html', form=unForm, plateformes=toutesPlat)


        if not campagnes_existantes_sur_plat:
            # Création de la campagne
            campagne = Campagne(date=date_campagne.strftime('%Y-%m-%d'), duree=duree, nomPlateforme=nomPlateforme)
            db.session.add(campagne)
            db.session.commit()
         
            for p_id_str in personnes_ids:
                p_id = int(p_id_str)
                db.session.add(Participer(numCampagne=campagne.numCampagne, idP=p_id))
            
            db.session.commit()
            # flash("La campagne a été ajoutée avec succès!", 'success')
            return redirect(url_for('accueil'))
            
    # Si échec de la validation
    return render_template('ajout_camp.html', form=unForm, plateformes=toutesPlat)
     




    
@app.route('/plateformes/<nomPlateforme>/', methods=['GET','POST'])
@login_required
def detail_plateforme(nomPlateforme):
    user = Personne.query.get_or_404(current_user.idP)
    unForm = PlateformeForm()
    try:
        participer = Participer.query.filter(Participer.idP == user.idP).first()
        camp = Campagne.query.filter(Campagne.numCampagne==participer.numCampagne).first()
        plat = Plateforme.query.filter(Plateforme.nomPlateforme==camp.nomPlateforme).first()
        lab=Laboratoire.query.filter(Laboratoire.nomLab==plat.lab_id).first()
        toutePlat = Plateforme.query.filter(Plateforme.lab_id==lab.nomLab).all()
        nomPlat = [p.nomPlateforme for p in toutePlat]
        if not(nomPlateforme in nomPlat):
            return redirect(url_for('accueil'))

        plat = Plateforme.query.filter(Plateforme.nomPlateforme==nomPlateforme).first()
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
                objet = Equipement.query.filter(Equipement.idE==obj.idE).first()
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
    camp = Campagne.query.filter(Campagne.numCampagne==numCampagne).first()
    try:
        """participer = Participer.query.filter(Participer.idP == user.idP, Participer.numCampagne==numCampagne).first()
        camp = Campagne.query.filter(Campagne.numCampagne==numCampagne).first()
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
                personne = Personne.query.filter(Personne.idP==pers.idP).first()
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
            # Clé du dictionnaire est l'ID du fichier (en string, important pour le JS)
            all_file_details[str(fichier.idFichier)] = { 
                'idFichier': echantillon.idFichier,
                'idEchantillon': echantillon.numEchantillon,
                # Combiner typeE et nomSpecifique pour l'affichage de l'espèce
                'espece': f"{echantillon.typeE} ({echantillon.nomSpecifique})",
                'commentaire': echantillon.commentaire
            }

    # Déterminer les détails initiaux pour le pré-remplissage par Jinja
    initial_details = {
        'idFichier': 'N/A', 
        'idEchantillon': 'N/A',
        'espece': 'Sélectionner un fichier',
        'commentaire': ''
    }
    if all_file_details:
        first_id = list(all_file_details.keys())[0]
        initial_details = all_file_details[first_id]

    return render_template('fichier_sequence.html', 
                           campagne=campagne,
                           fichiers=fichiers, 
                           initial_details=initial_details,
                           all_file_details=all_file_details,
                           random=random)

    