import os
import fonctions_utiles as fu
from adn import *

class Espece:
    def __init__(self, nom):
        self.nom=nom
        self.filles=[]

    def is_hypothetique(self)-> bool:
        """
        Precise si l'espèce est hypothètique

        Args:
            self: l'espèce à verifier

        Returns:
            True si l'espèce est hypothètique, False sinon.
        """
        return not self.filles==[]

    def get_filles(self)-> list:
        """
        Retourne les espèces filles si l'espèce analysée est avérée

        Args:
            self: l'espèce à verifier

        Returns:
            La liste des espèces filles
        """
        assert(self.is_hypothetique()), print("Votre espèce n'a pas de filles")
        return self.filles


class EspeceAveree(Espece):
    def __init__(self, nom_fichier: str):
        nom=os.path.basename(nom_fichier).replace('.adn', '')
        super().__init__(nom)
        try:
            self.adn_sequence = fu.transformer_fichier(nom_fichier)
            if not self.adn_sequence:
                raise ValueError("Le fichier ADN est vide.")
        except FileNotFoundError:
            print(f"ERREUR: Le fichier {nom_fichier} n'a pas été trouvé.")
            raise
        except Exception as e:
            print(f"ERREUR lors du chargement de {nom_fichier}: {e}")
            raise

    def get_adn(self)-> str:
        """
        Retourne la séquence adn du fichier .adn liée à l'espèce

        Args:
            self: l'espèce à verifier

        Returns:
            la séquence adn de l'espèce
        """
        return self.adn_sequence
    
class EspeceHypothetique(Espece):
    def __init__(self, espece1: Espece, espece2: Espece):
        nom=f'({espece1.nom}+{espece2.nom})'
        super().__init__(nom)
        self.filles = [espece1, espece2]

    def get_adn(self):
        return None
    

def distance_especes(espece_a: Espece, espece_b: Espece)-> int: 
    """
    Calcule la distance entre les deux espèces selon si elles sont hypthètiques ou non

    Args:
        espece_a: la première espèce 
        espece_b: la deuxième espèce

    Returns:
        La distance entre les séquences adn des espèces.
    """
    if espece_a.is_hypothetique() and espece_b.is_hypothetique():
        fille1_a, fille2_a = espece_a.get_filles()
        d1=distance_especes(fille1_a, espece_b)
        d2=distance_especes(fille2_a, espece_b)
        return (d1+d2)/2
    
    elif espece_b.is_hypothetique():
        fille1_b, fille2_b=espece_b.get_filles()
        d1=distance_especes(espece_a, fille1_b)
        d2=distance_especes(espece_a, fille2_b)
        return (d1+d2)/2
    elif espece_a.is_hypothetique():
        fille1_a, fille2_a=espece_a.get_filles()
        d1=distance_especes(espece_b, fille1_a)
        d2=distance_especes(espece_b, fille2_a)
        return (d1+d2)/2
    
    else: 
        return distance_levenshtein(espece_a.get_adn(), espece_b.get_adn())
    

def reconstruire_arbre_phylogenetique(especes_initiales: list[EspeceAveree]) -> Espece:
    """
    Reconstruit l'arbre phylogénétique en utilisant la méthode des plus petites distances.

    Args:
        especes_initiales: Liste des espèces avérées (EspeceAveree) avec leur ADN.

    Returns:
        L'espèce hypothétique racine de l'arbre (EspeceHypothetique).
    """
    especes_restantes = list(especes_initiales)
    while len(especes_restantes) >= 2:
        min_distance = float('inf')
        paire_proche = None
        
        for i in range(len(especes_restantes)):
            for j in range(i + 1, len(especes_restantes)):
                espece_a = especes_restantes[i]
                espece_b = especes_restantes[j] 
                distance = distance_especes(espece_a, espece_b)
                
                if distance < min_distance:
                    min_distance = distance
                    paire_proche = (i, j)
        if paire_proche is not None:
            i, j = paire_proche
            espece1 = especes_restantes[i]
            espece2 = especes_restantes[j]
            nouvel_ancetre = EspeceHypothetique(espece1, espece2)
         
            print(f"Fusion de '{espece1.nom}' et '{espece2.nom}' (Distance: {min_distance:.2f})")
            if i > j:
                especes_restantes.pop(i)
                especes_restantes.pop(j)
            else:
                especes_restantes.pop(j)
                especes_restantes.pop(i)
    
            especes_restantes.append(nouvel_ancetre)
            print(f"Nouvel ancêtre : '{nouvel_ancetre.nom}'. Espèces restantes : {len(especes_restantes)}")
    if especes_restantes:
        return especes_restantes[0]
    else:
        return None


def visualiser_arbre(racine: Espece, niveau=0, prefixe="Root: "):
    """
    Affiche l'arbre phylogénétique de manière récursive.
    """
    if racine is None:
        return ""
    visuel = " " * (niveau * 4) + prefixe + racine.nom + "\n"
    if racine.is_hypothetique():
        filles = racine.get_filles()
        if len(filles) == 2:
            visuel += visualiser_arbre(filles[0], niveau + 1, "├── ")
            visuel += visualiser_arbre(filles[1], niveau + 1, "└── ")
        elif len(filles) == 1:
            visuel += visualiser_arbre(filles[0], niveau + 1, "│-- ")
    return visuel