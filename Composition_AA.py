#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import scipy.stats as st

from Info_imp import FASTA

#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

def composition_AA(PDB):
    seq,_ = FASTA(PDB)
    seq = seq.replace("\n", "")
    dico = {}
    for AA in seq:
        if AA not in dico.keys():
            dico[AA] = 1
        else:
            dico[AA] += 1

    for AA in dico.keys():
        dico[AA] = round(dico[AA]/len(seq)*100, 2)

    #Transformation du dictionnaire pour l'utiliser facilement pour le graphique (futur tableau pandas)
    dico_remanie = {}
    #Futur colone Acide aminé
    dico_remanie["AA"] = list(dico.keys())
    #Futur colonne Frequence
    dico_remanie["Freq"] = list(dico.values())

    return dico_remanie

def tableau_bilan_AA(PDB):

    # Importation du tableaur contenant les valeurs de références d'Uniprot
    dF = pd.read_excel("valeurs_freqAA.xlsx")
    # Création du dataframe de la fréquences des AA dans la séquence
    dictio = composition_AA(PDB)
    Df = pd.DataFrame(dictio)

    #Fusion des tableaux selon la colonne AA
    df_fusio = pd.merge(dF, Df, on='AA', how='outer')
    # On comble par des 0 les valeurs manquantes potentielles
    df_fusio = df_fusio.fillna(0)

    return df_fusio


def test_proportion(dataframe):
    liste_mat = []
    for i in range(len(dataframe)):
        mat = np.array([[dataframe['Freq'][i], dataframe["FreqRef"][i]],
                    [100-dataframe['Freq'][i], 100-dataframe["FreqRef"][i]]])
        liste_mat.append(mat)

    liste_pvalue = []
    for table in liste_mat:
        _, pvalue = st.fisher_exact(table, alternative = "two-sided")
        liste_pvalue.append(pvalue)
    return liste_pvalue




def graphique_aa(PDB):

    #Récupération du tableau
    df = tableau_bilan_AA(PDB)
    p_value = test_proportion(df)

    #Initiation d'un jeu de couleur pour le graphique grâce au module Seaborn
    couleur = sb.color_palette('Set2', n_colors=len(df['AA']))
    sb.set()
    #Création des histogrammes

    # Figsize pour la taille de la fenetre
    ax = df.plot(x='AA', kind= "bar" , figsize=(10, 8), color= couleur , edgecolor = "black")
    # Choisi le maximum entre la colonne des Freq et des fréquences de références
    ymax = np.maximum(df["Freq"].max(), df["FreqRef"].max())
    # Ajuste les axes des y pour ne pas que les annotations se superposent à la légende
    ax.set_ylim(0, ymax+4)


    i = 0
    for bar in ax.patches:
        if i == 20:
            break
        if p_value[i]<0.05:
            texte = "*"
        else:
            texte = "ns"
        ax.text(bar.get_x() + bar.get_width(),
            ymax,
            texte,
            ha='center',
            color='black',  # couleur du texte
            fontsize=12,  # taille de la police
            fontweight='light')  # poids de la police
        i +=1

    # Étiqueter les axes et le titre
    plt.xlabel('Acides Aminés')
    plt.ylabel('Fréquence')
    plt.title('Fréquences des acides aminés dans la séquence protéique')
    plt.legend()
    plt.show()
    
    return plt.show()
