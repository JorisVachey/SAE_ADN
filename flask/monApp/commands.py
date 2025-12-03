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

@app.cli.command()
@click.argument('prenom')
@click.argument('nom')
@click.argument('poste')
@click.argument('pwd')
def newuser (prenom, nom,poste,pwd):
    '''Adds a new user'''
    from . models import Personne
    from hashlib import sha256
    m = sha256()
    m.update(pwd.encode())
    unUser = Personne(prenom=prenom ,nom=nom,poste=poste,mdp =m.hexdigest())
    db.session.add(unUser)
    db.session.commit()
    lg.warning('User ' + prenom+ nom + ' created!')

#flask newuser Jean Dupont directeur 123456 
#flask newuser Joris Vachey chercheur azerty 
#flask newuser Nolan Morain technicien aaa 

@app.cli.command("seed-db")
def seed_db():
    try:
        # --- 1. Laboratoires ---
        lab1 = Laboratoire(nomLab="LIRMM", adresse="Montpellier", budget=1500000)
        lab2 = Laboratoire(nomLab="LAMIH", adresse="Valenciennes", budget=800000)
        db.session.add_all([lab1, lab2])

        # --- 2. Plateformes ---
        pf1 = Plateforme(nomPlateforme="NanoFab", nbPersonnes=5, cout=5000, intervalleMaintenance=90,derniereMaintenance = "2025-10-01",prochaineMaintenance="2025-11-02")
        pf1.laboratoire = lab1 
        
        pf2 = Plateforme(nomPlateforme="RoboTest", nbPersonnes=3, cout=2000, intervalleMaintenance=30, derniereMaintenance=None, prochaineMaintenance=None)
        pf2.laboratoire = lab2

        pf3 = Plateforme(nomPlateforme="ThermoScan", nbPersonnes=2, cout=1000, intervalleMaintenance=180, derniereMaintenance="2025-05-15", prochaineMaintenance="2025-11-11")
        pf3.laboratoire = lab1 # Attaché au LIRMM
        
        db.session.add_all([pf1, pf2, pf3])
        db.session.commit() 

        # --- Équipements ---
        eq1 = Equipement(nomEquipement="Microscope Électronique")
        eq2 = Equipement(nomEquipement="Sonde de Température")
        eq3 = Equipement(nomEquipement="Bras Robotique KUKA")
        eq4 = Equipement(nomEquipement="Spectromètre Raman")
        eq5 = Equipement(nomEquipement="Chambre Climatique")
        eq6 = Equipement(nomEquipement="Imprimante 3D Métal")
        
        db.session.add_all([eq1, eq2, eq3, eq4, eq5, eq6])
        db.session.commit() # Obtient les IDs des équipements (idE)

        # --- Contenir (Plateforme -> Équipement) ---
        c1 = Contenir(nomPlateforme=pf1.nomPlateforme, idE=eq1.idE)
        c2 = Contenir(nomPlateforme=pf1.nomPlateforme, idE=eq2.idE)
        c3 = Contenir(nomPlateforme=pf2.nomPlateforme, idE=eq3.idE)
        c4 = Contenir(nomPlateforme=pf3.nomPlateforme, idE=eq4.idE) # ThermoScan -> Spectromètre
        c5 = Contenir(nomPlateforme=pf3.nomPlateforme, idE=eq5.idE) # ThermoScan -> Chambre Climatique
        c6 = Contenir(nomPlateforme=pf1.nomPlateforme, idE=eq6.idE) # NanoFab -> Imprimante 3D
        c7 = Contenir(nomPlateforme=pf2.nomPlateforme, idE=eq5.idE) # RoboTest -> Chambre Climatique (partagé)
        
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7])

        # --- Habilitations ---
        h1 = Habilitation(type="Électrique")
        h2 = Habilitation(type="Chimique")
        h3 = Habilitation(type="Radiations")
        h4 = Habilitation(type="Biologique")
        db.session.add_all([h1, h2, h3,h4])

        # --- Nécessite (Plateforme -> Habilitation) ---
        n1 = Necessite(type=h1.type, nomPlateforme=pf1.nomPlateforme) # NanoFab -> Électrique
        n2 = Necessite(type=h3.type, nomPlateforme=pf1.nomPlateforme) # NanoFab -> Radiations
        n3 = Necessite(type=h4.type, nomPlateforme=pf2.nomPlateforme) # RoboTest -> Biologique
        n4 = Necessite(type=h2.type, nomPlateforme=pf3.nomPlateforme) # ThermoScan -> Chimique
        n6 = Necessite(type=h2.type, nomPlateforme=pf1.nomPlateforme) # NanoFab -> Chimique
        
        db.session.add_all([n1, n2, n3, n4, n6])
        
        # --- Campagnes ---
        camp1 = Campagne(date="2025-12-01", duree=7,nomPlateforme = pf1.nomPlateforme,lieu="Orléans")
        camp2 = Campagne(date="2026-01-15", duree=3,nomPlateforme = pf2.nomPlateforme,lieu="Forêt")
        camp3 = Campagne(date="2026-03-20", duree=10, nomPlateforme=pf1.nomPlateforme, lieu="Grenoble")
        camp4 = Campagne(date="2025-11-25", duree=2, nomPlateforme=pf3.nomPlateforme, lieu="Sous-Sol")
        camp5 = Campagne(date="2026-04-05", duree=5, nomPlateforme=pf2.nomPlateforme, lieu="Toulouse")
        
        db.session.add_all([camp1, camp2, camp3, camp4, camp5])
        db.session.commit() # Obtient les IDs des campagnes (numCampagne)

        # --- Posséder (Personne -> Habilitation) ---
        pos1 = Posseder(type=h1.type, idP=1) # idP 1: Électrique
        pos2 = Posseder(type=h2.type, idP=2) # idP 2: Chimique
        pos3 = Posseder(type=h2.type, idP=1) # idP 1: Chimique
        pos4 = Posseder(type=h3.type, idP=3) # idP 3: Radiations
        pos5 = Posseder(type=h4.type, idP=1) # idP 1: Biologique
        pos7 = Posseder(type=h1.type, idP=3) # idP 3: Électrique
        
        db.session.add_all([pos1, pos2, pos3, pos4, pos5, pos7])

        # --- Participer (Campagne -> Personne) ---
        part1 = Participer(numCampagne=camp1.numCampagne, idP=1) # Campagne 1 -> idP 1
        part2 = Participer(numCampagne=camp1.numCampagne, idP=2) # Campagne 1 -> idP 2
        part3 = Participer(numCampagne=camp2.numCampagne, idP=3) # Campagne 2 -> idP 3
        part4 = Participer(numCampagne=camp3.numCampagne, idP=1) # Campagne 3 -> idP 1
        part6 = Participer(numCampagne=camp4.numCampagne, idP=2) # Campagne 4 -> idP 2
        part9 = Participer(numCampagne=camp5.numCampagne, idP=3) # Campagne 5 -> idP 3
        db.session.add_all([part1, part2, part3, part4,  part6, part9])

        # --- Fichiers ---
        f1 = Fichier(nomFichier="Résultats_NanoFab_1201.pdf")
        f2 = Fichier(nomFichier="Analyse_Acier_C40_Ref.pdf")
        f3 = Fichier(nomFichier="Rapport_ThermoScan_1125.txt")
        f4 = Fichier(nomFichier="Photos_Campagne3_Grenoble.zip")
        f5 = Fichier(nomFichier="Note_Prepa_Campagne5.docx")

        db.session.add_all([f1,f2,f3,f4,f5])
        db.session.commit()

        # --- Échantillons ---
        ech1 = Echantillon(typeE="Polymère", nomSpecifique="PPC-1", commentaire="Test initial", numCampagne=camp1.numCampagne, idP=1)
        ech2 = Echantillon(typeE="Métal", nomSpecifique="Acier C40", commentaire="Échantillon de référence", numCampagne=camp2.numCampagne, idP=3)
        ech3 = Echantillon(typeE="Polymère", nomSpecifique="PPC-1", commentaire="Reprise du test initial", numCampagne=camp1.numCampagne, idP=1)
        ech4 = Echantillon(typeE="Verre", nomSpecifique="Verre QZ-1", commentaire="Échantillon pour Spectromètre", numCampagne=camp3.numCampagne, idP=1)
        ech5 = Echantillon(typeE="Bois", nomSpecifique="Chêne traité", commentaire="Test de vieillissement", numCampagne=camp3.numCampagne, idP=3)
        ech6 = Echantillon(typeE="Polymère", nomSpecifique="PVC souple", commentaire="Test de température extrême", numCampagne=camp4.numCampagne, idP=2)
        ech7 = Echantillon(typeE="Métal", nomSpecifique="Alliage Titane", commentaire="Test de résistance RoboTest", numCampagne=camp5.numCampagne, idP=2)
        ech8 = Echantillon(typeE="Liquide", nomSpecifique="Éthanol Pur", commentaire="Contrôle qualité", numCampagne=camp1.numCampagne, idP=3)
        ech9 = Echantillon(typeE="Bois", nomSpecifique="Chêne non traité", commentaire="Référence pour test de vieillissement", numCampagne=camp3.numCampagne, idP=3)


        db.session.add_all([ech1, ech2, ech3, ech4, ech5, ech6, ech7, ech8, ech9]) 
        
        ech1.fichier = f1 
        ech2.fichier = f2
        ech6.fichier = f3 
        ech5.fichier = f4
        # ech7 n'a pas de fichier associé
        
        db.session.commit()
        print("✅ Base de données peuplée avec des données de test additionnelles !")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du peuplement de la base de données : {e}")