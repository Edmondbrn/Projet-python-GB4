#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================


def header(PDB):
    """
    Fonction créant le header de la séquence en format FASTA à partir des informations de la fiche PDB.
    input: fiche pdb en str
    ouput: header en str (nom de l'organisme et identifiant uniprot)
    """
    # Initiation de la varibale contenant le header
    seq = ">"
    PDB = PDB.split("\n")
    for ligne in PDB:
        # Informations clés dans la 1er ligne DBREF de la fiche pdb uniquement
        if "DBREF" in ligne :
            ligne = ligne.split()
            seq += ligne[6] +  "|" +ligne[7] + "\n"
            # S'arrête si plus de 1 ligne DBREF
            break
    return seq

def FASTA(PDB):
    """
    Extraction des acides aminés à partir de la fiche PDB afin de créer le format FASTA de la séquence.
    Input: fiche pdb en str
    Output: seéquence fasta en str et liste des AA à 3 lettres ou tuple de booléens (garde le même nombre de sortie, 2) si la séquence n'a pas pu être chargée
    """
    # Création d'une liste pour parcourir plus facilement en la coupant à chaque retour à la ligne
    PDB = PDB.strip()
    PDB = PDB.split("\n")
    # Création de la liste pour stocker les AA de la séquence
    liste_AA = []

    # Parcour du début du fichier tant qu'on n'a pas croisé SEQRES
    i = 0
    while "SEQRES" not in PDB[i] and i+1<len(PDB):
        i+=1
    # Ce qu'il se passe si la séquence est bien résolue
    if i+1<len(PDB):
        #Récupération des résidus sur les lignes SEQRES et arrêt du parcous dès que les lignes SEQRES s'arrêtent
        while "SEQRES"  in PDB[i]:
            # Slicing de la ligne pour récupérer les résidus facilement
            ligne = PDB[i].split()
            # Ajout de l'acide aminé (pas .append() pour éviter d'avoir une liste de liste)
            liste_AA+= ligne[4:]
            i+=1

        code_acide_amine = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"}


        # Création de la liste pour accueillir la séquence à une lettre
        liste_AA_1_Lettre = []
        for AA in liste_AA:
            try: # test si l'AA est un AA officiel, des fois il y a des AA étranges dans SEQRES (ex: PHQ)
                liste_AA_1_Lettre.append(code_acide_amine[AA])
            except:
                continue

        #Code pour insérer un retour à la ligne tous les 80 AA
        if len(liste_AA_1_Lettre) > 80:
            for i in range(1, (len(liste_AA_1_Lettre)//80)+1):
                liste_AA_1_Lettre.insert(80*i +i-1 ,"\n")

        #Création de la chaine de caractères

        seq_FASTA = "".join(liste_AA_1_Lettre)

        return seq_FASTA, liste_AA

    else: 
        return (False, False)


def fusion(PDB):
    """
    Création du format FASTA comprenant la séquence en acides aminés et le header.
    Input: fiche pdb en str
    Output: sequence au format FASTA en str ou message d'erreur en str
    """
    Header = header(PDB)
    seq,_ = FASTA(PDB)
    # Si la séquence existe bien
    if seq:
        sequence = Header + seq
        return sequence
    else:
        return "Aucune séquence détéctée, veuillez vérifier votre fiche pdb"

def info_imp(PDB) :
    '''Création du fichier comprenant toutes les informations importantes sur la séquence étudiée.
    Informations importantes : header, séquence, taille de la séquence, identifiant uniprot, méthode expérimentale, résolution.
    Input: fiche pdb en str
    Output: message d'erreur en str ou  str avec le texte descriptif'''
    # initiation de la liste de stockage et du test pour DBREF
    liste_info = []
    test = True
    PDB = PDB.strip()
    PDB = PDB.split("\n")
    for ligne in PDB:
        ligne = ligne.split()
        # On recupère le header de la fiche
        if ligne[0] == "HEADER" :
            liste_info.append("Description: " + " ".join(ligne[1:]))
        # recupération du titre
        if "TITLE" in ligne:
            liste_info.append("Titre:" +  " ".join(ligne[1:]))
        # recupération du nombre de résidus et de l'identifiant uniprot mais que le premier dbref
        if ligne[0] == "DBREF" :
            if test:
                liste_info.append("Taille de la séquence " + ligne[4] + " résidus")
                liste_info.append("Identifiant Uniprot " + ligne[6])
                test = False
            else:
                continue
        # Méthode d'analyse
        if "EXPDTA" in ligne:
            liste_info.append("Méthode expérimentale: " + " ".join(ligne[1:]))
        if "REMARK" in ligne and "RESOLUTION." in ligne:
            liste_info.append("Résolution: " + ligne[3] + " ANGSTROMS")
    # Message d'erreur si la liste est vide
    if liste_info == []:
        return "Vérifier l'intégrité de la fiche pdb"
    # mise en forme du texte
    else:
        info = ""
        for element in liste_info:
            info += element + "\n"
        return info