#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


from Composition_AA import tableau_bilan_AA
from Info_imp import fusion, info_imp
from coordonnees_atome import pontdisulfure
from Profil_hydrophobicite import hydrophobicite
import os
import pandas as pd

#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================
def classification(AA, Classification, PDB, chemin_py, repertoire): 
    #on définit une fonction classification prenant en compt 3 arguments : un AA spécifique, un critère de classification, et le paramètre PDB 
    """
    Classification des acides aminés en fonction de leur polarité, acidité, basicité, poids, fréquence d'apparition.
    Définition dictionnaire code des acides aminés : 3L to 1L
    Input: Acide aminé en str, la classification choisie en str (voir dans application.py), la fiche pdb en str, le repertoire de travail générral et le repertoire du lieu d'enregistrement des résultats en str
    Output: Nouvelle valeur du b factor  (float)

    """
    if Classification == "polarite":  
        # Définition de groupes d'acides aminés en fonction de leur polarité
        polaires_non_charges = ('SER', 'THR', 'ASN', 'GLN', 'CYS')
        polaires_acides =  ('ASP', 'GLU')
        polaires_basiques = ('LYS', 'ARG', 'HIS')
        apolaires_non_aromatiques = ('GLY', 'ALA', 'VAL', 'LEU', 'ILE', 'PRO',"MET")
        apolaires_aromatiques = ('PHE', 'TYR', 'TRP')
        # Création d'un dictionnaire associant chaque groupe à une valeur
        dico_polarité = {polaires_non_charges: 1, polaires_acides: 200, polaires_basiques: 400, apolaires_non_aromatiques: 600, apolaires_aromatiques : 800}
         # Si le critère de classification est "polarite", on vérifie à quel groupe appartient l'acide aminé spécifié et renvoie la valeur associée à ce groupe dans le dictionnaire dico_polarité
        for element in dico_polarité.keys():
            if AA in element:
                return round(dico_polarité[element], 2)
    
    elif Classification == "poids":
        # On crée un dictionnaire associant chaque acide aminé à son poids moléculaire
        poids_moleculaires_aa = {'ALA': 89.09,'ARG': 174.20,'ASN': 132.12,'ASP': 133.10,'CYS': 121.15,
                                 'GLN': 146.15, 'GLU': 147.13, 'GLY': 75.07, 'HIS': 155.16, 'ILE': 131.18,
                                 'LEU': 131.18, 'LYS': 146.19, 'MET': 149.21, 'PHE': 165.19, 'PRO': 115.13, 
                                 'SER': 105.09,'THR': 119.12, 'TRP': 204.23, 'TYR': 181.19, 'VAL': 117.15}
        #Si le critère de classification est "poids", la fonction renvoie le poids moléculaire de l'acide aminé spécifié multiplié par 4
        return round(poids_moleculaires_aa[AA]*4, 2)

    elif Classification == "frequence":
         # On appelle une fonction externe "tableau_bilan_AA" avec le paramètre PDB
        df = tableau_bilan_AA(PDB, chemin_py, repertoire)
        # On crée le dictionnaire associant chaque acide aminé à sa représentation en une lettre
        code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}
        acide_amine_1_lettre = code_acide_amine[AA]
        # Sélectionne la ligne pour l'acide aminé dans la colonne fréquence
        donnee = df.loc[df["AA"]== acide_amine_1_lettre]["Freq"]
        # Renvoie uniquement la valeur arrondie de la fréquence
        return round(donnee.iloc[0]*10, 2)
    



def fichier_pdb(PDB, Classification, code_pdb, repertoire, chemin_py):
    """
    Création d'un nouveau fichier qui contiendra notre classification des acides aminés par ligne et leur B-factor correspondant.
    Input: fiche pdb, classification choisie, code pdb de la fiche, repertoire de travail général et celui du dossier de la fiche en question, tous en str
    Output: nouveau fichier pdb (str) pour la coloration selon les b factor sur pymol
    
    """
    # Fixe repertoire dans le dossier de la fiche
    os.chdir(repertoire)
    fh = open("nouveau_fichier{}.pdb".format(code_pdb),'w')
    PDB2 = PDB.split("\n")
    for line in PDB2:
        # lignes avec un b factor
        if line[0:4] == "ATOM":
            # on récupère l'acide aminé (coupe la première lettre si plusieurs formes, ex: ALEU, BLEU pour une leucine)
            AA = line[17:20]
            nv_B_Factor = classification(AA, Classification, PDB, chemin_py, repertoire)
            # Mise en place des espaces selon la taille du b factor
            if len(str(round(nv_B_Factor))) >= 3:
                espace = ""
            elif len(str(round(nv_B_Factor))) >=2 and len(str(round(nv_B_Factor))) < 3 :
                espace = " "
            else:
                espace = "  "
            # création de la ligne avec le nouveau b factor et en gardant la même mise en page que la ligne d'origine
            nvline = line[:60] + espace + "{:.2f}".format(nv_B_Factor) + line[-12:-1] + line[-1]
            fh.write(nvline + "\n")
        # On reprend toutes les lignes n'entrant pas en compte dans les coordonnées/b factor des atomes
        else:
            fh.write(line + "\n")
    fh.close()
    return fh


def mise_en_page(titre):
    """
    Création d'une nouvelle mise en page de notre nouveau fichier bilan.
    Input: Titre de l'en-tête au format str
    Output: En tête en str
    """
    texte_separation = "="*200 +"\n" + " "*90 + titre + "\n" + "="*200 + "\n"*2
    return texte_separation

def fichier_bilan(PDB, nom_fiche, repertoire, chemin):
    """ 
    Création d'un fichier bilan sur notre séquence d'interet comprenant toutes les informations importantes sur la séquence.
    fiche bilan : Info importantes, seq FASTA, proportions aa, hydrophobicité protéine, présence de ponts disulfures.
    Input: fiche pdb, code pdb de la fiche, repertoire générale et chemin du dossier des analyses de la fiche au format str
    Output: Création du fichier .txt bilan
    """
    tableau = tableau_bilan_AA(PDB, chemin, repertoire)
    # Indique d'enregistrer le fichier dans le dossier propre à la fiche
    os.chdir(repertoire)
    fh = open("Fichier bilan {}.txt".format(nom_fiche),"w", encoding= "utf-8")
    fh.write(mise_en_page("Séquence FASTA"))
    fh.write(fusion(PDB) + "\n"*2)

    fh.write(mise_en_page("Informations importantes"))
    fh.write(info_imp(PDB) + "\n"*2)

    fh.write(mise_en_page("Analyse des proportions des acides aminés"))
    # test si la fonction renvoie le booléen négatif (erreur)
    if not isinstance(tableau, pd.DataFrame):
        fh.write("Un problème a eu lieu avec votre fiche pdb.\nVeuillez la recharger correctement\n\n")
    else:
        fh.write(str(tableau)+ "\n"*2)

    fh.write(mise_en_page("Valeur de l'hydrophobicité de la protéine"))
    valeur_hydro = hydrophobicite(PDB)
    if not valeur_hydro:
        fh.write("Un problème a eu lieu avec votre fiche pdb.\nVeuillez la recharger correctement\n\n")
    else:
        i=1
        for element in valeur_hydro:
            fh.write(str(i) + "   " +  str(round(element, 3)) + "\n")
            i +=1
        fh.write("\n"*2)

    fh.write(mise_en_page("Pontdisulfures"))
    dico_Distance = pontdisulfure(PDB, "SG")
    # Si la fonction renvoie la str d'erreur
    if type(dico_Distance) == str:
        fh.write("Aucun cystéine n'est présente dans votre séquence.\nVérifier l'intégrité de votre fichier pdb au cas où.")
    # Récupération des dictionnaires
    else:
        _, dico_ptdi, dico_non_ptdi = dico_Distance
        for element in dico_ptdi.keys():
            fh.write("Les cystéines suivantes sont liées: " + element + " à une distance de: " + str(round(dico_ptdi[element], 2)) + "A\n")
        for element in dico_non_ptdi.keys():
            fh.write("Les cystéines suivantes ne sont pas liées: " + element + "à une distance de: " + str(round(dico_non_ptdi[element], 2)) + "A\n")


    return fh.close()