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


@app.cli.command("seed-db")
def seed_db():
    try:
        # --- 1. Laboratoires ---
        lab1 = Laboratoire(nomLab="LIRMM", adresse="Montpellier", budget=1500000)
        lab2 = Laboratoire(nomLab="LAMIH", adresse="Valenciennes", budget=800000)
        db.session.add_all([lab1, lab2])

        # --- 2. Plateformes ---
        pf1 = Plateforme(nomPlateforme="NanoFab", nbPersonnes=5, cout=5000, intervalleMaintenance=90, lieu="Bâtiment A")
        pf1.derniereMaintenance = "2025-10-01"
        pf1.laboratoire = lab1
        
        pf2 = Plateforme(nomPlateforme="RoboTest", nbPersonnes=3, cout=2000, intervalleMaintenance=30, lieu="Halle Ouest")
        pf2.derniereMaintenance = "2025-11-05"
        pf2.laboratoire = lab2

        db.session.add_all([pf1, pf2])
        db.session.commit() # Commit intermédiaire pour avoir les IDs des plateformes

        # --- 3. Équipements ---
        eq1 = Equipement(nomEquipement="Microscope Électronique")
        eq2 = Equipement(nomEquipement="Sonde de Température")
        eq3 = Equipement(nomEquipement="Bras Robotique KUKA")
        db.session.add_all([eq1, eq2, eq3])
        db.session.commit() # Commit intermédiaire pour avoir les IDs des équipements

        # --- 4. Contenir (Plateforme -> Équipement) ---
        c1 = Contenir(nomPlateforme=pf1.nomPlateforme, idE=eq1.idE)
        c2 = Contenir(nomPlateforme=pf1.nomPlateforme, idE=eq2.idE)
        c3 = Contenir(nomPlateforme=pf2.nomPlateforme, idE=eq3.idE)
        db.session.add_all([c1, c2, c3])

        # --- 5. Habilitations ---
        h1 = Habilitation(type="Électrique")
        h2 = Habilitation(type="Chimique")
        h3 = Habilitation(type="Radiations")
        h4 = Habilitation(type="Biologique")
        db.session.add_all([h1, h2, h3,h4])

        # --- 6. Nécessite (Plateforme -> Habilitation) ---
        n1 = Necessite(type=h1.type, nomPlateforme=pf1.nomPlateforme)
        n2 = Necessite(type=h3.type, nomPlateforme=pf1.nomPlateforme)
        n3 = Necessite(type=h4.type, nomPlateforme=pf2.nomPlateforme)
        db.session.add(n1)
        db.session.add(n2)
        db.session.add(n3)
        
        # --- 7. Campagnes ---
        camp1 = Campagne(date="2025-12-01", duree=7)
        camp1.nomPlateforme = pf1.nomPlateforme
        
        camp2 = Campagne(date="2026-01-15", duree=3)
        camp2.nomPlateforme = pf2.nomPlateforme
        
        db.session.add_all([camp1, camp2])
        db.session.commit() # Commit intermédiaire pour avoir les IDs des campagnes

        # --- 8. Personnes ---
        p1 = Personne(nom="Dupont", prenom="Alice", poste="Chercheuse")
        p2 = Personne(nom="Martin", prenom="Bob", poste="Technicien")
        p3 = Personne(nom="Lefevre", prenom="Claire", poste="Stagiaire")
        db.session.add_all([p1, p2, p3])
        db.session.commit() # Commit intermédiaire pour avoir les IDs des personnes

        # --- 9. Posséder (Personne -> Habilitation) ---
        pos1 = Posseder(type=h1.type, idP=p1.idP)
        pos2 = Posseder(type=h2.type, idP=p2.idP)
        pos3 = Posseder(type=h2.type, idP=p1.idP)
        db.session.add_all([pos1, pos2,pos3])

        # --- 10. Participer (Campagne -> Personne) ---
        part1 = Participer(numCampagne=camp1.numCampagne, idP=p1.idP)
        part2 = Participer(numCampagne=camp1.numCampagne, idP=p2.idP)
        part3 = Participer(numCampagne=camp2.numCampagne, idP=p3.idP)
        db.session.add_all([part1, part2, part3])

        # --- 11. Fichiers ---
        f1 = Fichier(nomFichier="Résultats_NanoFab_1201.pdf")
        db.session.add(f1)
        db.session.commit()

        # --- 12. Échantillons ---
        ech1 = Echantillon(typeE="Polymère", nomSpecifique="PPC-1", commentaire="Test initial", numCampagne=camp1.numCampagne, idP=p1.idP)
        ech2 = Echantillon(typeE="Métal", nomSpecifique="Acier C40", commentaire="Échantillon de référence", numCampagne=camp2.numCampagne, idP=p3.idP)

        # Ajoutez les échantillons à la session IMMÉDIATEMENT
        db.session.add_all([ech1, ech2]) 

        # Maintenant, l'établissement de la relation n'émettra plus d'avertissement
        ech1.fichier = f1 

        db.session.commit()
        print("✅ Base de données peuplée avec des données de test !")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors du peuplement de la base de données : {e}")