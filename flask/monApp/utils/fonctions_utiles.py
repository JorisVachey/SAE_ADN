import random
import os

NUCLEOTIDES = ['A','T','G','C']

def transformer_fichier(fichier: str)-> str:
    """
    Permet de passer un fichier en fichier .adn
    Args:
        fichier : fichier ADN d'entrée

    Returns:
        le fichier.adn
    """
    if not fichier.endswith('.adn'):
        fichier += '.adn'
    with open(fichier, 'r', encoding='utf8') as f:
        chaine_adn = f.read().strip()
        return chaine_adn
    
def generer_sequence(res: str, longueur: int, nucleotides: list) -> str:
    """
    Génère une séquence ADN aléatoire en ajoutant des nucléotides à une séquence existante.

    Args:
        res (str): séquence de départ à compléter.
        longueur (int): nombre de nucléotides à ajouter.
        nucleotides (list): liste des nucléotides possibles (ex: ['A', 'T', 'G', 'C']).

    Returns:
        str: séquence ADN complète après ajout des nucléotides aléatoires.
    """
    for _ in range(longueur):
        res += random.choice(nucleotides)
    return res

def charger_adn(adn: str) -> str:
    """
    Charge une séquence ADN depuis un fichier ou renvoie la chaîne si c'est déjà une séquence.

    Args:
        adn (str): nom du fichier ADN ou séquence ADN brute.

    Raises:
        FileNotFoundError: si le fichier spécifié n'existe pas.

    Returns:
        str: la séquence ADN sous forme de chaîne.
    """
    if not adn.endswith('.adn'):
        if os.path.exists(adn+".adn") :
            adn = transformer_fichier(adn)
    if adn.endswith(".adn"):
        if os.path.exists(adn):
            adn = transformer_fichier(adn)
        else: 
            raise FileNotFoundError(f"Le fichier {adn} n'existe pas")
    return adn