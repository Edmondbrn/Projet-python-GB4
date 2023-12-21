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
from math import sqrt



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

    code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}


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

    return seq_FASTA, liste_AA

def fusion(PDB):
    Header = header(PDB)
    seq,_ = FASTA(PDB)
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
            liste_info.append("Identifiant Uniprot " + ligne[6])
        if "EXPDTA" in ligne:
            liste_info.append("Méthode expérimentale: " + " ".join(ligne[1:]))
        if "REMARK" in ligne and "RESOLUTION." in ligne:
            liste_info.append("Résolution: " + ligne[3] + " ANGSTROMS")

    info = ""
    for element in liste_info:
        info += element + "\n"
    return info

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

    #Graphique pour les acides aminés de la séquence
    plt.bar(df["AA"], df["Freq"], color = couleur, edgecolor = "black")
    plt.title("Histogramme réprésentant la répartition des acides aminés dans la séquence")
    plt.xlabel("Acides aminés")
    plt.ylabel("Fréquence (%)")


    plt.show()



def hydrophobicite(seq):
    pass



def coordonnees(PDB, atom):
    """Fonction qui extrait les coordonnées dans l'espace d'un atome précis donné"""
    _, seq = FASTA(PDB)
    # seq = list(seq.replace("\n",""))

    if atom == "SG":
        atome = "C"
    else:
        atome = "CA"
    PDB = PDB.split("\n")
    i = 0
    # indice_seq = 0
    # index_corr = 0
    longueur_seq_resolue = 0

    dico_atome = {}
    while  PDB[i][0:4] != "ATOM":
        i+=1
    while PDB[i][0:4] == "ATOM" or PDB[i+1][0:4] == "ATOM" :
        ligne = PDB[i].split()
        # test si SG ou CA est dans la séquence
        if atom in ligne:
            
            # Si l'AA est annoté sous plusieurs états différents
            if len(ligne[3]) > 3:
                # Si AA est en plusieurs etats différents (ALEU/BLEU)
                ligne_bis = PDB[i+1].split()
                ligne_a_compter = 1
                liste_x = [float(ligne[6])]
                liste_y = [float(ligne[7])]
                liste_z = [float(ligne[8])]

                nbr_de_ligne_bis = 1
                # Parcourt toutes les lignes avec les potentiels variants des AA et ajoute les coordonnées
                while atom in ligne_bis:
                    liste_x.append(float(ligne_bis[6]))
                    liste_y.append(float(ligne_bis[7]))
                    liste_z.append(float(ligne_bis[8]))
                    ligne_a_compter += 1
                    ligne_bis = PDB[i+ligne_a_compter].split()
                    nbr_de_ligne_bis += 1
                # moyenne des coordonnées des deux états
                x, y, z, pos = np.mean(liste_x) , np.mean(liste_y), np.mean(liste_z),  ligne[5]
                dico_atome[atome + "MOY" + pos] = [round(x,3) , round(y,3), round(z,3)]
                longueur_seq_resolue += 1
                # Saute le 2e CA de l'AA dans le second état ou plus
                i += nbr_de_ligne_bis
                
            else:
                x, y, z, pos= ligne[6], ligne[7], ligne[8], ligne[5]
                dico_atome[atome + pos] = [x,y,z]
                longueur_seq_resolue += 1
                # Passe à la ligne suivante si elle commence par ATOM
                if PDB[i+1][0:4] == "ATOM": 
                    i += 1
                # Si on a une ligne ANISOU entre les lignes ATOm, on la passe
                else:
                    i += 2
        # Si la ligne ne contient pas CA ou SG, on passe à celle d'après
        else:
            i+=1
    return dico_atome, longueur_seq_resolue


def calcul_distance(PDB, atom):
    """Calcul la distance euclidienne entre 2 atomes donnés"""
    dico_coord,_ = coordonnees(PDB, atom)
    dico_distance = {}
    # Nombre de tour de boucle à sauter
    k = 1
    for atome in dico_coord.keys():
        liste_coord_ref = dico_coord[atome]

        # Stocke le nombre de tours déjà sauter
        y = 0
        for atome_compl in dico_coord.keys():
            # Saute les boucles
            if y < k :
                y+=1
                continue
                
            distance = (float(dico_coord[atome_compl][0]) - float(liste_coord_ref[0]))**2 + (float(dico_coord[atome_compl][1]) - float(liste_coord_ref[1]))**2 + (float(dico_coord[atome_compl][2]) - float(liste_coord_ref[2]))**2
            distance = sqrt(distance)
            dico_distance[atome + ":" + atome_compl] = distance
        k +=1
    return dico_distance

def recuperation_code_Uniprot(PDB):
    """Récupère le code Uniprot de la protéine de la fiche PDB"""
    info_importante = info_imp(PDB)
    info_importante = info_importante.strip()
    info_importante = info_importante.split("\n")
    info_Uniprot = info_importante[-1].split()
    code_uniprot = info_Uniprot[-1]
    return code_uniprot


def importation_online_uniprot(PDB):
    """ Charge le fichier txt de la fiche uniprot de la protéine"""
    code = recuperation_code_Uniprot(PDB)
    """Fonction pour récupérer la fiche uniprot en ligne"""
    liste_fich = []
    try:
        context = ssl._create_unverified_context()
        u=urllib.request.urlopen("https://rest.uniprot.org/uniprotkb/" + code.upper()+".txt", context=context)
        pdblines=u.readlines()
        u.close()
    except:
        return("Problème lors de la lecture du fichier: \n" + "https://rest.uniprot.org/uniprotkb/"+code.upper()+".txt\n Veuillez fermer le programme et réessayer")
    else:
        for ligne in pdblines:
            liste_fich.append(ligne.decode("utf8").strip() + "\n")
            fichier = "".join(liste_fich)
        return fichier


def secreted(PDB):
    """Vérifie si la protéine est sécrétée"""
    uniprot = importation_online_uniprot(PDB)
    info_loc=[]
    uniprot= uniprot.split("\n")
    for ligne in uniprot:
        if "SUBCELLULAR LOCATION: Secreted" in ligne :
            return True
        else:
            False


def pontdisulfure(PDB, atom):
    """Calcule la présence ou non de pontdisulfure entre les protéines"""
    
    if secreted(PDB):
        dico_distance = calcul_distance(PDB, atom)

        if dico_distance == {}:
            return "Aucun cystéine n'est présente dans votre séquence"

        dico_pontdi = {}
        dico_non_pont = {}
        for atome in dico_distance.keys():
            if dico_distance[atome] <= 3:
                dico_pontdi[atome] = dico_distance[atome]
            else:
                dico_non_pont[atome] = dico_distance[atome]
        return dico_pontdi, dico_non_pont
    
    else:
        dico_distance = calcul_distance(PDB, atom)

        if dico_distance == {}:
            return "Aucun cystéine n'est présente dans votre séquence"
        
        dico_pontdi = {}
        dico_non_pont = {}
        for atome in dico_distance.keys():
            if dico_distance[atome] <= 3:
                dico_pontdi[atome] = dico_distance[atome]
            else:
                dico_non_pont[atome] = dico_distance[atome]
        return dico_pontdi, dico_non_pont

        #return "Etes vous sûr que la protéine est sécrétée avant de calculer la présence de pontdisulfures ?"



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
        



def fichier_pdb(PDB, Classification):
    fh = open("newfichier.pdb",'w')
    PDB2 = PDB.split("\n")
    for line in PDB2:
        if line[0:4] == "ATOM":
            AA = line[17:20]
            nv_B_Factor = classe(AA, Classification, PDB)
            nvline = line[:61] + str(nv_B_Factor) + line[-12:-1]
            fh.write(nvline + "\n")
        else:
            fh.write(line + "\n")
    fh.close()
    return fh


def mise_en_page(titre):
    texte_separation = "="*200 +"\n" + " "*90 + titre + "\n" + "="*200 + "\n"*2
    return texte_separation

def fichier_bilan(PDB):
    fh = open("Fichier bilan.txt","w", encoding= "utf-8")
    fh.write(mise_en_page("Séquence FASTA"))
    fh.write(fusion(PDB) + "\n"*2)

    fh.write(mise_en_page("Informations importantes"))
    fh.write(info_imp(PDB) + "\n"*2)

    fh.write(mise_en_page("Analyse des proportions des acides aminés"))
    fh.write(str(tableau_bilan_AA(PDB))+ "\n"*2)

    fh.write(mise_en_page("Pontdisulfures"))
    dico_ptdi, dico_non_ptdi = pontdisulfure(PDB, "SG")
    for element in dico_ptdi.keys():
        fh.write("Le cystéines suivantes sont liées: " + element + " à une distance de: " + str(round(dico_ptdi[element], 2)) + "A\n")
    for element in dico_non_ptdi.keys():
        fh.write("Le cystéines suivantes ne sont pas liées:" + element + "à une distance de: " + str(round(dico_non_ptdi[element], 2)) + "A\n")


    return fh.close()








#====================================================================================================================

                                                    # Script #

#====================================================================================================================

# fiche_pdb = importation_online("1GC6")
# print(fiche_pdb)
# print(distance_carbone_alpha(fiche_pdb))
# print(matrice_contact(fiche_pdb))
# print(coordonnees(fiche_pdb, "CA"))
# print(pontdisulfure(fiche_pdb, "SG"))
# print(graph_matrice(fiche_pdb))
# print(fichier_pdb(fiche_pdb, "polarite"))
# print(pontdisulfure(fiche_pdb, "SG"))
# print(fichier_bilan(fiche_pdb))
# print(secreted(fiche_pdb))

# Dico_distance = calcul_distance(dico)


# print(recuperation_code_Uniprot(fiche_pdb))
# print(importation_online_uniprot(fiche_pdb))

# df = (tableau_bilan_AA(fiche_pdb))


# print(composition_AA(fiche_pdb))

# print(graphique_aa(fiche_pdb))

# print(info_imp(fiche_pdb))

#print(fusion(fiche_pdb))
# print(FASTA(fiche_pdb))

# print(info_imp(fiche_pdb))




# https://github.com/Edmondbrn/Projet-python-GB4
