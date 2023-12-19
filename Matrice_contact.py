#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import scipy.stats as st

from Info_imp import FASTA
from Composition_AA import tableau_bilan_AA
from coordonnees_atome import *



#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

def distance_carbone_alpha(PDB):
    distance_CA = calcul_distance(PDB, "CA")
    return distance_CA

def matrice_contact(PDB):
    _, longueur_mat = coordonnees(PDB, "CA")
    index = [x for x in range(1, longueur_mat+1)]
    
    distance = distance_carbone_alpha(PDB)
    liste_distance = list(distance.values())
    df = pd.DataFrame(index = index, columns= index)
    np.fill_diagonal(df.values, float(0))

    # indice pour la liste des distances
    k = 0
    # Parcourt des lignes du tableau 
    for i in range(len(df.columns)):
        # position de la cellule
        pos_cel = 1+i
        while pos_cel < df.shape[1] and k< len(liste_distance):
            df.iloc[i,pos_cel] = liste_distance[k]
            df.iloc[pos_cel,i]= liste_distance[k]
            pos_cel +=1
            k+=1
  
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    

    return df

def graph_matrice(PDB):
    
    mat = matrice_contact(PDB)
    # Conversion du datframe en un format compréhensible pour le graphiUe
    mat = mat.astype(float)

    # Initiation du graphique matplotlib
    f, ax = plt.subplots(figsize=(20, 16))

    # Création du dégradé de couleur avec seaborn
    cmap = sb.color_palette("rainbow", as_cmap=True)

    # contour = plt.imshow(mat, cmap="jet", alpha=1, interpolation = "quadric")
    contour = plt.contourf(mat, cmap = cmap,levels = 7, alpha = 1)

    # Ajouter une barre de couleur pour le tracé de contour
    legende = plt.colorbar(contour, ax=ax, orientation="vertical", shrink=0.75)
    legende.set_label('Distance (A)', rotation=90, labelpad=15)
    plt.xlabel("Index des acides aminés")
    plt.ylabel("Index des acides aminés")
    plt.title("Heatmap de la distance des acides aminés dans l'espace")

    return plt.show()


def classe(AA, classification, PDB):

    if classification == "polarite":
        polaires_non_charges = ('SER', 'THR', 'ASN', 'GLN', 'CYS')
        polaires_acides =  ('ASP', 'GLU')
        polaires_basiques = ('LYS', 'ARG', 'HIS')
        apolaires_non_aromatiques = ('GLY', 'ALA', 'VAL', 'LEU', 'ILE', 'PRO',"MET")
        apolaires_aromatiques = ('PHE', 'TYR', 'TRP')
        dico_polarité = {polaires_non_charges: 1, polaires_acides: 200, polaires_basiques: 400, apolaires_non_aromatiques: 600, apolaires_aromatiques : 800}
        for element in dico_polarité.keys():
            if AA in element:
                return dico_polarité[element]
    
    elif classification == "poids":
        poids_moleculaires_aa = {'ALA': 89.09,'ARG': 174.20,'ASN': 132.12,'ASP': 133.10,'CYS': 121.15,
                                 'GLN': 146.15, 'GLU': 147.13, 'GLY': 75.07, 'HIS': 155.16, 'ILE': 131.18,
                                 'LEU': 131.18, 'LYS': 146.19, 'MET': 149.21, 'PHE': 165.19, 'PRO': 115.13, 
                                 'SER': 105.09,'THR': 119.12, 'TRP': 204.23, 'TYR': 181.19, 'VAL': 117.15}
        return poids_moleculaires_aa[AA]*4

    elif classification == "frequence":
        df = tableau_bilan_AA(PDB)
        code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}
        acide_amine_1_lettre = code_acide_amine[AA]
        # Sélectionne la ligne pour l'acide aminé dans la colonne fréquence
        donnee = df.loc[df["AA"]== acide_amine_1_lettre]["Freq"]
        # Renvoie uniquement la valeur de la fréquence
        return round(donnee.iloc[0])