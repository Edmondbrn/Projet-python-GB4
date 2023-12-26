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
            ligne = str(ligne)
            if ">" not in ligne and "," not in ligne and ";" not in ligne and "{" not in ligne and "//" not in ligne and "Expasy" not in ligne and "}" not in ligne and "|" not in ligne :
                liste_fich.append(ligne.strip() + "\n")
                fichier = "".join(liste_fich)
        return fichier


def extraction_data(tableau) :
    dico_hydrophobicite = {}
    tableau = tableau.split("\n")
    for line in tableau:
        line = line.split()
        if len(line)>=2:
            dico_hydrophobicite[line[0][0:3].upper()] = line[1]
    return dico_hydrophobicite
        
    


def hydrophobicite(PDB):
    """Fonction qui permet de calculer les hydrophobicités moyennes d'une séquence au format FASTA
    input: sequence au format FASTA
    Output: liste contenant les hydrophobicités moyennes"""
    _, seq = FASTA(PDB)
    liste_moyenne_hydrophobicite = []
    # Récupération du dictionnaire avec les valeurs de référence d'hydrophobicité
    dico_hydro = extraction_data(lecture_hydophobicite())
    for i in range (0, len(seq)-8):
        fenetre = seq[i:i+9]
        liste_hydrophobicite = []
        for aa in fenetre:
            liste_hydrophobicite.append(float(dico_hydro[aa]))
        liste_moyenne_hydrophobicite.append(np.mean(liste_hydrophobicite))
   
    return liste_moyenne_hydrophobicite
    

def graphique_hydro(PDB):

    liste_hydro  = hydrophobicite(PDB)
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