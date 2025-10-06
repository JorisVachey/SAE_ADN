import random
import os

def generer_adn(nom_fichier : str, longueur : int):
    chemin = os.getcwd + nom_fichier
    res = ""
    liste_adn=['A','T','G','C']
    if os.path.exists(chemin):
        return "le chemin existe déjà, voulez vous l'écraser ? o/n"
        
    for _ in range(longueur):
        res += random.choice(liste_adn)
    with open(f"{nom_fichier}.adn", "w", encoding = "utf8") as f :
        f.write(res)