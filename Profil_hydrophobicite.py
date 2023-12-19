#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================

import urllib.request
import ssl
import sys
import platform
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from Info_imp import FASTA
from Recuperation_fichier import importation_locale



#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

fiche_pdb = importation_locale("1CRN")
_, seq = FASTA(fiche_pdb)


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
        
    


def hydrophobicite(sequence):
    """Fonction qui permet de calculer les hydrophobicités moyennes d'une séquence au format FASTA
    input: sequence au format FASTA
    Output: liste contenant les hydrophobicités moyennes"""
    liste_moyenne_hydrophobicite = []
    
    dico_hydro = extraction_data(lecture_hydophobicite())
    for i in range (0, len(sequence)-9):
        fenetre = sequence[i:i+9]
        liste_hydrophobicite = []
        for aa in fenetre:
            liste_hydrophobicite.append(float(dico_hydro[aa]))
        liste_moyenne_hydrophobicite.append(np.mean(liste_hydrophobicite))
    return liste_moyenne_hydrophobicite
    
liste = hydrophobicite(seq)
sb.lineplot(liste)
plt.show()

    