# SAE_ADN
SAE 1 du premier semestre de la 2e année

# Membres
Nolan Morain — chef de projet 

Tifany Meunier

Joris Vachey

# Changement entre rendu 1 et rendu 3 sur le cahier des charges:
la base de données a légèrement été changée pour faciliter la gestion des échantillons et du lieu de la campagne.
Les maquettes ont été changées pour être en rapport avec l'esthétique finale de notre app.

# Fonctionnalitées:
Gestion des plateformes de fouille

Gestion des campagnes de fouille

Planification des campagnes (date, lieu, personnel, plateforme)

Gestion des habilitations et maintenances

Upload des échantillons ADN

Analyse des séquences (Levenshtein, mutations, comparaisons)

Gestion du budget annuel du laboratoire

# Installation
git clone https://github.com/.../SAE_ADN
cd SAE_ADN
pip install -r requirements.txt

# Initialisation
flask init-db
flask newuser Jean Dupont directeur 123456
flask newuser Joris Vachey chercheur azerty
flask newuser Nolan Morain technicien aaa
flask seed-db
