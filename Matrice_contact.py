#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
from pyreadr import write_rds

from coordonnees_atome import calcul_distance, coordonnees



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
    f, ax = plt.subplots(figsize=(10, 8))

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

def fichier_matrice(matrice, extension, nom_fiche_pdb):
    if extension == "xlsx":
        matrice.to_excel('Matrice de contact de {}.xlsx'.format(nom_fiche_pdb), index=False)
    elif extension == "csv":
        matrice.to_csv('Matrice de contact de {}.csv'.format(nom_fiche_pdb), index=False)
    else:
        write_rds('Matrice de contact de {}'.format(nom_fiche_pdb), matrice)
    return "Le fichier {} contenant la matrice de contact a bien été enregistré".format(extension)

