#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================


def header(PDB):
    '''Fonction créant le header de la séquence en format FASTA à partir des informations de la fiche PDB.'''
    seq = ">"
    PDB = PDB.split("\n")
    for ligne in PDB:
        if "DBREF" in ligne :
            ligne = ligne.split()
            seq += ligne[6] +  "|" +ligne[7] + "\n"
    return seq

def FASTA(PDB):
    '''Extraction des acides aminés à partir de la fiche PDB afin de créer le format FASTA de la séquence.'''
    # Création d'une liste pour parcourir plus facilement en la coupant à chaque retour à la ligne
    PDB = PDB.strip()
    PDB = PDB.split("\n")
    # Création de la liste pour stocker les AA de la séquence
    liste_AA = []

    # Parcour du début du fichier tant qu'on n'a pas croisé SEQRES
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
    '''Création du format FASTA comprenant la séquence en acides aminés et le header.'''
    Header = header(PDB)
    seq,_ = FASTA(PDB)
    sequence = Header + seq
    return sequence

def info_imp(PDB) :
    '''Création du fichier comprenant toutes les informations importantes sur la séquence étudiée.
    Informations importantes : header, séquence, taille de la séquence, identifiant uniprot, méthode expérimentale, résolution.'''
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