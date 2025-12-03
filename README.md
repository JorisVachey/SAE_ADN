# SAE_ADN
SAE 1 du premier semestre de la 2e année

# Membres
Nolan — chef de projet 

Tifany 

Joris

# Changement entre rendu 1 et rendu 3 sur le cahier des charges:
la bd a légèrement changé pour faciliter la gestion des echantillons et du lieu de la campagne.
Les maquettes ont été changées pour être en rapport avec l'hestétique final de notre app.

# Fonctionnalitées:
Gestion des plateformes de fouille

Planification des campagnes (dates, lieux, personnel, plateforme)

Gestion des habilitations et maintenance

Upload des échantillons ADN

Analyse des séquences (Levenshtein, mutations, comparaisons)

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
