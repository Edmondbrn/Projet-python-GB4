import Fonction as F
import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import seaborn as sb

def test_proportion(PDB):

    pdb = F.importation_online(PDB)
    df = F.tableau_bilan_AA(pdb)

    liste_mat = []
    for i in range(len(df)):
        mat = np.array([[df['Freq'][i], df["FreqRef"][i]],
                    [100-df['Freq'][i], 100-df["FreqRef"][i]]])
        liste_mat.append(mat)
    print(liste_mat)

    liste_pvalue = []
    for table in liste_mat:
        if np.any(table < 5) :
            res = st.fisher_exact(table, alternative = "two-sided")
            liste_pvalue.append(res.pvalue)

        else:
            _ ,pvalue ,_ ,_ = st.chi2_contingency(table)
            liste_pvalue.append(pvalue)
    print(liste_pvalue)
    return liste_pvalue


df = F.tableau_bilan_AA(F.importation_online("1H4W"))

#Initiation d'un jeu de couleur pour le graphique grâce au module Seaborn
couleur = sb.color_palette('Set2', n_colors=len(df['AA']))
sb.set()
#Création des histogrammes

# Création de l'axe pour contenir 2 graphiques à la fois
# fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# Figsize pour la taille de la fenetre
ax = df.plot(x='AA', kind= "bar" , figsize=(10, 6) , color = couleur ,edgecolor = "black"),


liste  = test_proportion("1H4W")

i = 0
for bar in ax.patches:
    if i == 20:
        break
    if liste[i]<0.05:
        texte = "*"
    else:
        texte = "ns"

    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width(),
        13,
        texte,
        ha='center',
        color='black',  # couleur du texte
        fontsize=14,  # taille de la police
        fontweight='light')  # poids de la police
    i +=1

# Étiqueter les axes et le titre
plt.xlabel('Acides Aminés')
plt.ylabel('Fréquence')
plt.title('Fréquences des Acides Aminés dans la Séquence Protéique')
plt.legend()
plt.show()