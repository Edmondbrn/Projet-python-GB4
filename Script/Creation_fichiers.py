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
    '''Classification des acides aminés en fonction de leur polarité, acidité, basicité, poids, fréquence d'apparition.
    Définition dictionnaire code des acides aminés : 3L to 1L'''
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
                return dico_polarité[element]
    
    elif Classification == "poids":
        # On crée un dictionnaire associant chaque acide aminé à son poids moléculaire
        poids_moleculaires_aa = {'ALA': 89.09,'ARG': 174.20,'ASN': 132.12,'ASP': 133.10,'CYS': 121.15,
                                 'GLN': 146.15, 'GLU': 147.13, 'GLY': 75.07, 'HIS': 155.16, 'ILE': 131.18,
                                 'LEU': 131.18, 'LYS': 146.19, 'MET': 149.21, 'PHE': 165.19, 'PRO': 115.13, 
                                 'SER': 105.09,'THR': 119.12, 'TRP': 204.23, 'TYR': 181.19, 'VAL': 117.15}
        #Si le critère de classification est "poids", la fonction renvoie le poids moléculaire de l'acide aminé spécifié multiplié par 4
        return poids_moleculaires_aa[AA]*4

    elif Classification == "frequence":
         # On appelle une fonction externe "tableau_bilan_AA" avec le paramètre PDB
        df = tableau_bilan_AA(PDB, chemin_py, repertoire)
        # On crée le dictionnaire associant chaque acide aminé à sa représentation en une lettre
        code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}
        acide_amine_1_lettre = code_acide_amine[AA]
        # Sélectionne la ligne pour l'acide aminé dans la colonne fréquence
        donnee = df.loc[df["AA"]== acide_amine_1_lettre]["Freq"]
        # Renvoie uniquement la valeur arrondie de la fréquence
        return round(donnee.iloc[0])
    



def fichier_pdb(PDB, Classification, code_pdb, repertoire, chemin_py):
    '''Création d'un nouveau fichier qui contiendra notre classification des acides aminés par ligne et leur B-factor correspondant.'''
     # On change le répertoire de travail vers le répertoire spécifié
    os.chdir(repertoire)
    # On ouvre un nouveau fichier en mode écriture
    fh = open("nouveau_fichier{}.pdb".format(code_pdb),'w')
      # On supprime les sauts à la ligne contenus dans le fichier PDB2
    PDB2 = PDB.split("\n")
    # On parcourt chaque ligne du fichier PDB2
    for line in PDB2:
         # On vérifie si la ligne commence par "ATOM"
        if line[0:4] == "ATOM":
             # alors on extrait le code à 3lettress d'acide aminé (AA) de la ligne
            AA = line[17:20]
            # On appelle la fonction externe 'classification' pour obtenir et attribuer le nouveau B-factor
            nv_B_Factor = classification(AA, Classification, PDB, chemin_py, repertoire)
             # On construit une nouvelle ligne avec le B-factor modifié
            nvline = line[:61] + str(nv_B_Factor) + line[-12:-1]
             # On écrit la nouvelle ligne dans le fichier
            fh.write(nvline + "\n")
        else:
             # Si la ligne ne commence pas par "ATOM", on écrit la ligne telle quelle
            fh.write(line + "\n")
    fh.close()
    return fh


def mise_en_page(titre):
    '''Création d'une nouvelle mise en page de notre nouveau fichier PDB comprenant les B-factor des atomes.'''
    texte_separation = "="*200 +"\n" + " "*90 + titre + "\n" + "="*200 + "\n"*2
    return texte_separation

def fichier_bilan(PDB, nom_fiche, repertoire, chemin):
    ''' Création d'un fichier bilan sur notre séquence d'interet comprenant toutes les informations importantes sur la séquence.
    fiche bilan : Info importantes, seq FASTA, proportions aa, hydrophobicité protéine, présence de ponts disulfures.'''
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
            fh.write("Le cystéines suivantes sont liées: " + element + " à une distance de: " + str(round(dico_ptdi[element], 2)) + "A\n")
        for element in dico_non_ptdi.keys():
            fh.write("Le cystéines suivantes ne sont pas liées: " + element + "à une distance de: " + str(round(dico_non_ptdi[element], 2)) + "A\n")


    return fh.close()