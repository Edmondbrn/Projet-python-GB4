#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


# !python3
import urllib.request
import ssl
import sys
import platform

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import scipy.stats as st



#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================

def importation_online(code):
    """Fonction pour récupérer la fiche PDB en ligne"""
    liste_fich = []
    try:
        context = ssl._create_unverified_context()
        u=urllib.request.urlopen("https://files.rcsb.org/view/"+code.upper()+".pdb", context=context)
        pdblines=u.readlines()
        u.close()
    except:
        return("Problème lors de la lecture du fichier: \n" + "https://files.rcsb.org/view/"+code.upper()+".pdb\n Veuillez fermer le programme et réessayer")
    else:
        for ligne in pdblines:
            liste_fich.append(ligne.decode("utf8").strip() + "\n")
            fichier = "".join(liste_fich)
        return fichier


def importation_locale(code):
    """Fonction pour récupérer la fiche PDB en local"""
    liste_fich = []
    try:
        fh = open(code +".pdb", "r")
    except:
        return("Le fichier correspondant au code PDB {} n'a pas été trouvé\n Veuillez fermer le programme et réessayer".format(code))
    else:
        for ligne in fh:
            liste_fich.append(ligne)
        fh.close()
        Fichier = "".join(liste_fich)
        return Fichier
    
    
def header(PDB):
    seq = ">"
    PDB = PDB.split("\n")
    for ligne in PDB:
        if "DBREF" in ligne :
            ligne = ligne.split()
            seq += ligne[6] +  "|" +ligne[7] + "\n"
    return seq

def FASTA(PDB):

    # Création d'une liste pour parcourir plus facilement en la coupant à chaque retour à la ligne
    PDB = PDB.strip()
    PDB = PDB.split("\n")
    # Création de la liste pour stocker les AA de la séquence
    liste_AA = []

    # Parcous du début du fichier tant qu'on n'a pas croisé SEQRES
    i = 0
    while "SEQRES" not in PDB[i]:
        i+=1
    #Récupération des résidus sur les lignes SEQRES et arrêt du parcous dès que les lignes SEQRES s'arrêtent
    while "SEQRES"  in PDB[i]:
        # Slicing de la ligne pour récupérer les résidus facilement
        ligne = PDB[i].split()    
        # Ajout de l'acide aminé
        liste_AA+= ligne[4:]
        i+=1

    code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V",}   
    
        
    # Création de la liste pour accueillir la séquence à une lettre
    liste_AA_1_Lettre = []
    for AA in liste_AA:
        liste_AA_1_Lettre.append(code_acide_amine[AA])

    #Code pour insérer un retour à la ligne tous les 80 AA
    if len(liste_AA_1_Lettre) > 80:
        for i in range(1, (len(liste_AA_1_Lettre)//80)+1):
            liste_AA_1_Lettre.insert(80*i +i-1 ,"\n")

    #Création de la chaine de caractères
    
    seq_FASTA = "".join(liste_AA_1_Lettre)


    return seq_FASTA

def fusion(PDB):
    Header = header(PDB) 
    seq = FASTA(PDB)
    sequence = Header + seq
    return sequence

def info_imp(PDB) : 
    liste_info = []
    PDB = PDB.strip()
    PDB = PDB.split("\n")
    for ligne in PDB:
        ligne = ligne.split() 
        if ligne[0] == "HEADER" :
            liste_info.append("Description: " + " ".join(ligne[1:]))
        if "TITLE" in ligne:
            liste_info.append("Titre:" +  " ".join(ligne[1:]))
        if ligne[0] == "DBREF" :
            liste_info.append("Taille de la séquence " + ligne[4] + " résidus")
        if "EXPDTA" in ligne:
            liste_info.append("Méthode expérimentale: " + " ".join(ligne[1:]))
        if "REMARK" in ligne and "RESOLUTION." in ligne:
            liste_info.append("Résolution: " + ligne[3] + " ANGSTROMS")

    info = ""
    for element in liste_info:
        info += element + "\n"
    return info

def composition_AA(PDB):
    seq = FASTA(PDB)
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
        if np.any(table < 5) :
            res = st.fisher_exact(table, alternative = "two-sided")
            liste_pvalue.append(res[1])

        else:
            _ ,pvalue ,_ ,_ = st.chi2_contingency(table)
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
    
    #Graphique pour les acides aminés de la séquence
    plt.bar(df["AA"], df["Freq"], color = couleur, edgecolor = "black")
    plt.title("Histogramme réprésentant la répartition des acides aminés dans la séquence")
    plt.xlabel("Acides aminés")
    plt.ylabel("Fréquence (%)")


    plt.show()



def hydrophobicite(seq):
    pass


#====================================================================================================================

                                                    # Script #

#====================================================================================================================

fiche_pdb = importation_online("1IRC")
# print(fiche_pdb)

# df = (tableau_bilan_AA(fiche_pdb))


# print(composition_AA(fiche_pdb))

print(graphique_aa(fiche_pdb))

# print(info_imp(fiche_pdb))

#print(fusion(fiche_pdb))
# print(FASTA(fiche_pdb))

# print(info_imp(fiche_pdb))
