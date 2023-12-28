#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
from pyreadr import write_rds
import os

from coordonnees_atome import calcul_distance, coordonnees



#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

def distance_carbone_alpha(PDB):
    """Fonction qui calcule les distances entre les différents carbones alpha
    Input: fiche PDB en str
    Output: dictionnaire des paires de carbones alpha associés à un flottant représentant la distance en A"""
    distance_CA = calcul_distance(PDB, "CA")
    return distance_CA

def matrice_contact(PDB):
    """Fonction qui créée la matrice de contact entre les carbones alpha
    Input: fiche pdb en str
    Output: matrice/dataframe pandas"""
    # Recuperation du nombre d'atomes pour formater la matrice
    _, longueur_mat = coordonnees(PDB, "CA")
    index = [x for x in range(1, longueur_mat+1)]
    
    # Recupération des distances selon les pairs
    distance = distance_carbone_alpha(PDB)
    liste_distance = list(distance.values())
    # Création de la matrices avec une diagonale de 0 pour la distance des atomes avec eux-mêmes
    df = pd.DataFrame(index = index, columns= index)
    np.fill_diagonal(df.values, float(0))

    # indice pour la liste des distances
    k = 0
    # Parcourt de la matrice 
    for i in range(len(df.columns)):
        # position de la cellule
        pos_cel = 1+i
        # Parcourt de la matrice tant qu'on ne dépasse pas ses dimensions et celles de la liste contenant les distances
        while pos_cel < df.shape[1] and k< len(liste_distance):
            # Remplissage de la matrice en miroir (symétrie par rapport à la diagonale de 0)
            df.iloc[i,pos_cel] = liste_distance[k] # .iloc[index_ligne, index_colonne]
            df.iloc[pos_cel,i]= liste_distance[k]
            # Passage à la cellule suivante de la même colonne/ligne et à la paire d'atome suivante
            pos_cel +=1
            k+=1
    return df

def graph_matrice(PDB):
    """Fonction qi dessine le graphique (heatmap) de la matrice de contact
    Input: fiche pdb en str
    Output: graphique matplotlib"""
    
    mat = matrice_contact(PDB)
    # Conversion du datframe en un format compréhensible pour le graphique
    mat = mat.astype(float)
    # Initiation du graphique matplotlib
    f, ax = plt.subplots(figsize=(10, 8))
    # Création du dégradé de couleur avec seaborn
    cmap = sb.color_palette("rainbow", as_cmap=True)
    # Utilisation de la méthode contourf() de matplotlib pour dessiner le graphique
    contour = plt.contourf(mat, cmap = cmap,levels = 7, alpha = 1)

    # Ajouter une barre de couleur pour le graphique et une légende
    legende = plt.colorbar(contour, ax=ax, orientation="vertical", shrink=0.75)
    legende.set_label('Distance (A)', rotation=90, labelpad=15)
    plt.xlabel("Index des acides aminés")
    plt.ylabel("Index des acides aminés")
    plt.title("Heatmap de la distance des acides aminés dans l'espace")

    return plt.show()

def fichier_matrice(matrice, extension, nom_fiche_pdb, repertoire):
    """Fonction qui enregistre la matrice selon le format choisi par l'utilisateur
    Input: matrice de contact pandas (le format numpy devrait fonctionner également), le nom de l'extension (.xlsx, .csv, .rds)
           Et le nom de la fiche pdb en str pour nommer le fichier de sortie
    Output: Type de fichier choisi par l'utilisateur"""
    os.chdir(repertoire)
    # Création fichier xlsx et csv avec pandas directement
    if extension == "xlsx":
        matrice.to_excel('Matrice de contact de {}.xlsx'.format(nom_fiche_pdb), index=False)
    elif extension == "csv":
        matrice.to_csv('Matrice de contact de {}.csv'.format(nom_fiche_pdb), index=False)
    # Fichier rds avec la bibliothèque .rds
    else:
        write_rds('Matrice de contact de {}.rds'.format(nom_fiche_pdb), matrice)
    return "Le fichier {} contenant la matrice de contact a bien été enregistré".format(extension)


