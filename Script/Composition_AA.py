#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import scipy.stats as st
import os
import PyQt5

from Info_imp import FASTA

#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

def composition_AA(PDB):
    '''Fonction qui extrait la séquences en acides aminés de la fiche PDB et met les données dans un dictionnaire'''
    # Recuperation de la séquence FASTA
    seq,_ = FASTA(PDB)
    if seq:
        seq = seq.replace("\n", "")
        dico = {}
        # Comptage des AA
        for AA in seq:
            if AA not in dico.keys():
                dico[AA] = 1
            else:
                dico[AA] += 1
        # Transformation en fréquence d'apparition
        for AA in dico.keys():
            dico[AA] = round(dico[AA]/len(seq)*100, 2)

        #Transformation du dictionnaire pour l'utiliser facilement pour le graphique (futur tableau pandas)
        dico_remanie = {}
        #Futur colone Acide aminé
        dico_remanie["AA"] = list(dico.keys())
        #Futur colonne Frequence
        dico_remanie["Freq"] = list(dico.values())

        return dico_remanie
    
    else:
        return False

def tableau_bilan_AA(PDB, chemin, repertoire):
    '''Fonction qui va créer le tableau regroupant les fréquences en aa de notre séquence et les fréquences de références'''
    # Importation du tableaur contenant les valeurs de références d'Uniprot
    os.chdir(chemin)
    dF = pd.read_excel("valeurs_freqAA.xlsx")
    os.chdir(repertoire)
    # Création du dataframe de la fréquences des AA dans la séquence
    dictio = composition_AA(PDB)
    # test si la séquence existe / si les proportions ont pu être calculées
    if not dictio:
        return False
    else:
        Df = pd.DataFrame(dictio)

        #Fusion des tableaux selon la colonne AA
        df_fusio = pd.merge(dF, Df, on='AA', how='outer')
        # On comble par des 0 les valeurs manquantes potentielles
        df_fusio = df_fusio.fillna(0)

        return df_fusio


def test_proportion(dataframe):
    ''' Tests statistiques et test des proportions en acides aminés.'''

    liste_mat = []
    # Création des matrices pour comparer les fréquences
    for i in range(len(dataframe)):
                        # Fréquence positive
        mat = np.array([[dataframe['Freq'][i], dataframe["FreqRef"][i]],
                        # Fréquence négative
                    [100-dataframe['Freq'][i], 100-dataframe["FreqRef"][i]]])
        liste_mat.append(mat)

    liste_pvalue = []
    for table in liste_mat:
        # Test de fisher pour comparer les proportions
        _, pvalue = st.fisher_exact(table, alternative = "two-sided")
        liste_pvalue.append(pvalue)
    return liste_pvalue




def graphique_aa(PDB, repertoire, chemin):
    '''Création du graphique comprenant les valeurs du tableau de fréquences précédant.'''
    #Récupération du tableau
    df = tableau_bilan_AA(PDB, chemin, repertoire)
    if not isinstance(df, pd.DataFrame):
        return "Problème lors de la résolution de la séquence d'acide aminé.\nVeuillez vérifier votre fichier pdb."
    
    else:
        p_value = test_proportion(df)

        #Initiation d'un jeu de couleur pour le graphique grâce au module Seaborn
        couleur = sb.color_palette('Set1', n_colors=len(df['AA']))
        sb.set_theme(style="darkgrid")
        plt.switch_backend('Qt5Agg') # Cela transforme le graphique en élément interagique, peut poser problème si cela n'est pas spécifié sous certaines version de python (conflit fenêtre pygame et matplotlib, les autres graphiques le sont déjà à l'origine)

        # Création des histogrammes
        # Figsize pour la taille de la fenetre, edgecolor pour tracer le contour des barres
        ax = df.plot(x='AA', kind= "bar" , figsize=(10, 8), color= couleur , edgecolor = "black")

        # Choisi le maximum entre la colonne des Freq et des fréquences de références
        ymax = np.maximum(df["Freq"].max(), df["FreqRef"].max()) + 0.5
        # Ajuste les axes des y pour ne pas que les annotations se superposent à la légende
        ax.set_ylim(0, ymax+4)

        # Permet l'annotation des * ou ns sur le graphique
        i = 0
        # Parcourt des barres
        for bar in ax.patches:
            # On s'arrête aux 20 premières barres (21 correspond à la 2e du premier AA)
            if i == 20:
                break
            if p_value[i]<0.05:
                texte = "*"
            else:
                texte = "ns"
            # Fommatage du texte
            ax.text(bar.get_x() + bar.get_width(),
                ymax, # position en y
                texte,
                ha='center', # position par rapport à la barre
                color='black',  # couleur du texte
                fontsize=18,  # taille de la police
                fontweight='light')  # poids / (gras ou maigre) de la police
            i +=1

        # Étiqueter les axes et le titre
        plt.xlabel('Acides Aminés')
        plt.ylabel('Fréquence')
        plt.title('Fréquences des acides aminés dans la séquence protéique')
        plt.legend()
        plt.switch_backend('Qt5Agg')
        
        
        return plt.show()
