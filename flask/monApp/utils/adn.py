import random
import os
import numpy as np
from . import fonctions_utiles as fu

def generer_adn(nom_fichier : str, longueur : int):
    """
    Créer ou remplace un fichier contenant une séquence de longueur précisée en paramètres
    
    Args:
        nom_fichier: fichier ADN d'entrée
        longueur: longueur de la séquence adn voulue
    """
    if nom_fichier.endswith(".adn"):
        nom_fichier = nom_fichier[:-4]
    chemin = os.path.join(os.getcwd(), f"{nom_fichier}.adn")
    nom_final=""
    res = ""
    if os.path.exists(chemin):
        rep = input("Le fichier existe déjà, voulez vous l'écraser ? (o/n): ")
        if rep.lower() == "o":
            res = fu.generer_sequence(res, longueur, fu.NUCLEOTIDES)
            nom_final = nom_fichier
        else:
            while rep.lower() != "esc" and os.path.exists(chemin):
                rep = input("Veuillez entrer le nouveau nom de votre fichier ou 'esc' pour annuler: ")
                chemin = os.path.join(os.getcwd(), f"{rep}.adn")
                if not os.path.exists(chemin):
                    res = fu.generer_sequence(res, longueur, fu.NUCLEOTIDES)
                    nom_final = rep
                    break
                else:
                    print(f"Le fichier '{rep}.adn' existe déjà.")
    else:
        res = fu.generer_sequence(res, longueur, fu.NUCLEOTIDES)
        nom_final = nom_fichier

    adn_formate = ""
    largeur_ligne = 80
    for i in range(0, len(res), largeur_ligne):
        adn_formate += res[i:i+largeur_ligne] 
    
    with open(f"{nom_final}.adn", "w", encoding="utf8") as f:
        f.write(adn_formate)
    print(f"Fichier '{nom_final}.adn' créé avec succès!")

def muter_adn_remplacement(nom_fichier: str, proba_mutation: float, sortie: bool = True)-> tuple[str, int]:
    """
    Applique des remplacement de nucléotides aléatoires à une séquence ADN avec probabilité p.
    
    Args:
        nom_fichier: fichier ADN d'entrée
        proba_mutation: probabilité de mutation pour chaque nucléotide (0.0 à 1.0)
    Returns:
        nom_fichier_sortie et le nombre de remplacemment
    """
    if not nom_fichier.endswith('.adn'):
        nom_fichier += '.adn'
    if sortie:
        nom_fichier_sortie = nom_fichier.replace('.adn', f'_remplacement_{int(proba_mutation*100)}.adn')
    elif sortie is not True:
        nom_fichier_sortie = f"{nom_fichier}+_mute.adn"
    sequence_mutee = ""
    mutations_count = 0
    with open(nom_fichier, 'r', encoding='utf8') as f:
        for ligne in f:
            ligne = ligne.strip()
            ligne_mutee = ""
            for nucleotide in ligne:
                if nucleotide in fu.NUCLEOTIDES:
                    if random.random() < proba_mutation:
                        nouveaux_nucleotides = [n for n in fu.NUCLEOTIDES if n != nucleotide]
                        nucleotide_mute = random.choice(nouveaux_nucleotides)
                        ligne_mutee += nucleotide_mute
                        mutations_count += 1
                    else:
                        ligne_mutee += nucleotide
                else:
                    ligne_mutee += nucleotide
            sequence_mutee += ligne_mutee 
    
    with open(nom_fichier_sortie, 'w', encoding='utf8') as f:
        f.write(sequence_mutee)
    print(f"{mutations_count} remplacements terminés !")
    return nom_fichier_sortie, mutations_count

def muter_adn_deletion(nom_fichier: str, proba_mutation: float, sortie: bool = True)-> tuple[str, int]:
    """
    Applique des deletions aléatoires à une séquence ADN avec probabilité p.
    
    Args:
        nom_fichier: fichier ADN d'entrée
        proba_mutation: probabilité de mutation pour chaque nucléotide (0.0 à 1.0)
    Returns:
        nom_fichier_sortie et le nombre de suppressions
    """
    if not nom_fichier.endswith('.adn'):
        nom_fichier += '.adn'
    if sortie:
        nom_fichier_sortie = nom_fichier.replace('.adn', f'_deletion_{int(proba_mutation*100)}.adn')
    elif sortie is not True:
        nom_fichier_sortie = f"{nom_fichier}+_mute.adn"
    sequence_mutee = ""
    mutations_count = 0
    with open(nom_fichier, 'r', encoding='utf8') as f:
        for ligne in f:
            ligne = ligne.strip()
            ligne_mutee = ""
            for nucleotide in ligne:
                if nucleotide in fu.NUCLEOTIDES:
                    if random.random() < proba_mutation:
                        mutations_count += 1
                    else:
                        ligne_mutee += nucleotide
                else:
                    ligne_mutee += nucleotide
            sequence_mutee += ligne_mutee 
    with open(nom_fichier_sortie, 'w', encoding='utf8') as f:
        f.write(sequence_mutee)
    print(f"{mutations_count} deletions terminées !")
    return nom_fichier_sortie, mutations_count

def muter_adn_insertion(nom_fichier: str, proba_mutation: float, sortie: bool = True)-> tuple[str, int]:
    """
    Applique des insertions aléatoires à une séquence ADN avec probabilité p.
    
    Args:
        nom_fichier: fichier ADN d'entrée
        proba_mutation: probabilité de mutation pour chaque nucléotide (0.0 à 1.0)
    Returns:
        nom_fichier_sortie et le nombre d'insertions
    """
    if not nom_fichier.endswith('.adn'):
        nom_fichier += '.adn'
    if sortie:
        nom_fichier_sortie = nom_fichier.replace('.adn', f'_insertion_{int(proba_mutation*100)}.adn')
    elif sortie is not True:
        nom_fichier_sortie = f"{nom_fichier}+_mute.adn"
    sequence_mutee = ""
    nb_insert = 0
    with open(nom_fichier, 'r', encoding='utf8') as f:
        for ligne in f:
            ligne = ligne.strip()
            ligne_mutee = ""
            for nucleotide in ligne:
                if random.random() < proba_mutation:
                    nucleotide_mute = random.choice(fu.NUCLEOTIDES)
                    ligne_mutee += nucleotide_mute
                    nb_insert += 1
                ligne_mutee += nucleotide
            sequence_mutee += ligne_mutee
    with open(nom_fichier_sortie, 'w', encoding='utf8') as f:
        f.write(sequence_mutee)
    print(f"{nb_insert} insertions terminées !")
    return nom_fichier_sortie, nb_insert


import os

def mutations(nom_fichier: str, proba_r: float, proba_d: float, proba_i: float)-> tuple[str, list]:
    """
    Permet d'appliquer une ou plusieurs mutations sur un fichier ADN.
    Les fichiers intermédiaires sont supprimés : seul le fichier final est conservé.

    Args:
        nom_fichier: fichier ADN d'entrée
        proba_r: probabilité de mutation par remplacement pour chaque nucléotide (0.0 à 1.0)
        proba_d: probabilité de mutation par deletion pour chaque nucléotide (0.0 à 1.0)
        proba_i: probabilité de mutation par insertion pour chaque nucléotide (0.0 à 1.0)

    Returns:
        chemin du fichier final produit (ou le fichier d'entrée si aucune mutation appliquée)
        et le nombre de modifications
    """
    if nom_fichier.endswith('.adn'):
        base_name = nom_fichier[:-4]
    else:
        base_name = nom_fichier
        nom_fichier += '.adn'

    mutation = {
        'r': (muter_adn_remplacement, proba_r),
        'd': (muter_adn_deletion, proba_d),
        'i': (muter_adn_insertion, proba_i)
    }
    outputs = []
    current_input = nom_fichier
    nbModif = []

    for c in mutation.keys():
        func, p = mutation[c]
        if p <= 0:
            continue
        sortie, nb_mut = func(current_input, p, False)
        outputs.append(sortie)
        current_input = sortie
        nbModif.append(nb_mut)

    if len(outputs) > 1:
        for path in outputs[:-1]:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError:
                pass

    if outputs:
        final = outputs[-1]
        suffixe = random.randint(1000, 9999)
        final_name = f"{base_name}_mutations_{suffixe}.adn"
        os.rename(final, final_name)
        print(f"Traitement terminé. Fichier final : {final_name}")
        return final_name, nbModif
    else:
        print("Aucune mutation appliquée.")
        return nom_fichier, nbModif

def distance_remplacement_chaine(adn: str, adn_bis: str)-> int:
    """
    Calcule la distance entre deux séquence si il est possible de passer de l'une à l'autre en utilisant seulement de mutations par remplacement

    Args:
        adn: premier fichier ADN d'entrée
        adn_bis: deuxième fichier ADN d'entrée

    Returns:
        distance entre les deux séquences si il est possible de la calculer
    """
    try:
        adn = fu.charger_adn(adn)
        adn_bis = fu.charger_adn(adn_bis)
    except FileNotFoundError as e:
        print(e)
        return None

    assert(len(adn)==len(adn_bis)), "les fichiers ne doivent avoir subit que des mutations par remplacement"
    distance = 0
    for i in range(len(adn)):
        if adn[i]!=adn_bis[i]:
            distance+=1
    return distance

def distance_levenshtein(adn: str, adn_bis: str)-> int:
    """
    Calcule la distance entre deux séquence d'adn

    Args:
        adn: premier fichier ADN d'entrée
        adn_bis: deuxième fichier ADN d'entrée

    Returns:
        distance entre les deux séquences si il est possible de la calculer
    """
    try:
        adn = fu.charger_adn(adn)
        adn_bis = fu.charger_adn(adn_bis)
    except FileNotFoundError as e:
        print(e)
        return None
        
    x=len(adn)+1
    y=len(adn_bis)+1
    matrice=np.zeros((x,y))
    for i in range(x):
        matrice[i, 0]=i
    for j in range(y):
        matrice[0, j]=j
    for i in range(1,x):
        for j in range(1,y):
            if adn[i-1]==adn_bis[j-1]:
                cout_substitution=0
            else:
                cout_substitution=1
            matrice[i,j]=min(matrice[i-1,j]+1, matrice[i,j-1]+1, matrice[i-1,j-1]+cout_substitution)
    return matrice[x-1,y-1]

