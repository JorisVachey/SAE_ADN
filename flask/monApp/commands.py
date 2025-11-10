import click, logging as lg
from .app import app, db
from .models import *


@app.cli.command("init-db")
def init_db():
    # création de toutes les tables
    try:
        db.drop_all()
        db.create_all()
        print("✅ Base de données initialisée (tables créées) !")
    except Exception as e:
            db.session.rollback()
            print(f"Erreur lors de la création de l'administrateur : {e}")
