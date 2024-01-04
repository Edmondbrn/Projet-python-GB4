#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================

import urllib.request
import ssl

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

from Info_imp import FASTA
from Recuperation_fichier import importation_locale



#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================




def lecture_hydophobicite():
    '''

    Lecture d'un fichier comprenant le profil d'hydrophobicité sur le site internet protscale.
    input: None
    Output: tableau en str regroupant les hydrophobicités des AA
    '''
    liste_fich = []
    try:
        context = ssl._create_unverified_context()
        u=urllib.request.urlopen("https://web.expasy.org/protscale/pscale/Hphob.Fauchere.html", context=context)
        pdblines=u.readlines()
        u.close()
    except:
        return("Problème lors de la lecture du fichier")
    
    else:
        for ligne in pdblines:
            ligne = ligne.decode("utf8")
            # transformation html en str python
            ligne = str(ligne)
            # trie des lignes de la page html pour garder que le tableau
            if ">" not in ligne and "," not in ligne and ";" not in ligne and "{" not in ligne and "//" not in ligne and "Expasy" not in ligne and "}" not in ligne and "|" not in ligne :
                liste_fich.append(ligne.strip() + "\n")
            fichier = "".join(liste_fich)
                
        return fichier

def extraction_data(tableau) :
    '''
    Création d'un tableau comprenant les valeurs d'hydrophobicité pour chaque acides aminés.
    Input: tableau des hydrophobicités (str)
    Output: dictionnaire, clé AA en trois lettres et valeur hydrophobicité en str

    '''
    dico_hydrophobicite = {}
    tableau = tableau.split("\n")
    for line in tableau:
        line = line.split()
        # trie les lignes avec les données et les lignes vides
        if len(line)>=2:
            # AA et on récupère les 3 lettres           hydrophobicité
            dico_hydrophobicite[line[0][0:3].upper()] = line[1]
    return dico_hydrophobicite
        
    


def hydrophobicite(PDB):
    """Fonction qui permet de calculer les hydrophobicités moyennes d'une séquence au format FASTA.
    Input: sequence au format FASTA
    Output: liste contenant les hydrophobicités moyennes ou booléen si on a un problème avec la séquence fasta
    """
    # Récupération de la séquence en trois lettres
    _, seq = FASTA(PDB)
    if not seq:
        return False
    else:
        liste_moyenne_hydrophobicite = []
        # Récupération du dictionnaire avec les valeurs de référence d'hydrophobicité
        dico_hydro = extraction_data(lecture_hydophobicite())
        # fenêtre glissante de 9 aa
        for i in range (0, len(seq)-8):
            fenetre = seq[i:i+9]
            liste_hydrophobicite = []
            # Ajout de l'hydrophobicité de chaque AA
            for aa in fenetre:
                liste_hydrophobicite.append(float(dico_hydro[aa]))
            # Moyenne des ces hydrophobicités
            liste_moyenne_hydrophobicite.append(np.mean(liste_hydrophobicite))
    
        return liste_moyenne_hydrophobicite
    

def graphique_hydro(PDB):
    '''
    Création du graphique d'hydrophobicité en fonction de la position de la séquence et de l'hydrophobicité de chaque aa.
    input: fiche pdb en str
    output: graphique lineplot de seaborn (pyplot en plus simple et élégant) ou message d'erreur en str
    '''
    liste_hydro  = hydrophobicite(PDB)
    if not liste_hydro:
        return "Un problème a eu lieu avec la séquence d'acide aminé.\nVérifiez votre fichier pdb."
    # Configure le fond du graphique
    sb.set(style="whitegrid")
    # Fixe la taille de la fenêtre
    plt.figure(figsize=(12, 6))
    # Trace le graphique
    sb.lineplot(data=liste_hydro, marker="o", color="blue", label="Hydrophobicité")
    # Personnaliser les axes et le titre
    plt.xlabel("Position dans la séquence")
    plt.ylabel("Hydrophobicité")
    plt.title("Profil d'Hydrophobicité de la Protéine")

    # Afficher la légende
    plt.legend()
    # Afficher le graphique
    return plt.show()  