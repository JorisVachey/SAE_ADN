import flask
from .app import app,db
from flask import render_template, request, url_for , redirect, abort, jsonify
from hashlib import sha256
from flask_login import login_required, login_user, logout_user, login_manager, current_user
from .forms import *
from monApp.models import *
from monApp.forms import *
from sqlalchemy import desc
from datetime import date, datetime


@app.route('/')
def accueil() :
    return render_template('accueil.html')

@app.route('/connexion/')
def connexion() :
    return render_template('connexion.html')

#@app.route('/login/',methods=('GET','POST',))
#def login():
#    """
#    Gère la connexion des utilisateurs.
#
#    Si l'utilisateur est déjà connecté, il est redirigé vers le tableau de bord.
#    Lors de la soumission du formulaire, tente d'authentifier l'utilisateur.
#    En cas de succès, connecte l'utilisateur et le redirige.
#
#    :returns: Redirection vers le tableau de bord (si déjà connecté ou après connexion réussie)
#              ou le formulaire de connexion.
#    """
#    if current_user.is_authenticated:
#        return redirect(url_for('vue_dashboard'))
#    unForm = LoginForm ()
#    unUser=None
#    if not unForm.is_submitted():
#        unForm.next.data = request.args.get('next')
#    elif unForm.validate_on_submit():
#        unUser = unForm.get_authenticated_user()
#        if unUser:
#            login_user(unUser)
#            next = unForm.next.data or url_for("vue_dashboard")
#            return redirect(next)
#    return render_template('connexion.html',form=unForm)

@app.route('/ajout_plateforme/', methods=['GET', 'POST'])
def ajout_plat() :
    if request.method == 'POST':
        try:
            nomPlateforme = request.form.get('nomPlateforme')
            habilitation = request.form.get('habilitation')
            nbPersonnes = request.form.get("nbP")
            cout= request.form.get("coutPJ")
            intervalleMaintenance= request.form.get("interv")
            lieu= request.form.get("lieu")

            if not nomPlateforme or not habilitation or not nbPersonnes or not cout or not intervalleMaintenance or not lieu:
                return jsonify({'success': False, 'error': 'Champs manquants'}), 400
            
            plat_existant = Plateforme.query.filter_by(nomPlateforme=nomPlateforme).first()
            if plat_existant:
                return jsonify({'success': False, 'error': 'Une plateforme avec ce nom existe déjà.'}), 400

            try:
                prix_decimal = float(cout)
                nbPersonnes_int = int(nbPersonnes)
                intervalle = int(intervalleMaintenance)
            except ValueError:
                return jsonify({'success': False, 'error': 'Format de prix ou ID invalide'}), 400

            nouvelle_plat = Plateforme(
                nomPlateforme=nomPlateforme,
                nbPersonnes=nbPersonnes_int,
                cout=prix_decimal,
                intervalleMaintenance=intervalle,
                lieu=lieu,
            )

            db.session.add(nouvelle_plat)
            db.session.commit()
            

            return jsonify({
                'success': True,
                'plat': {
                    'id': nouveau_plat.idP,
                    'nomP': nouveau_plat.nomP,
                    'prixP': nouveau_plat.prixP,
                    'type_nom': type_nom,
                    'stock': nouveau_plat.stock,
                    'stockInit': nouveau_plat.stockInit
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500

    plats = Plat.query.all()
    types = Type_plat.query.all()
    return render_template("gestion_plat.html", plats=plats, types=types)