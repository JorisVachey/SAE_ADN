import flask
from .app import app,db
from flask import render_template, request, url_for , redirect, abort
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

@app.route('/plateforme/')
def plateforme() :
    return render_template('plateforme.html')


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

