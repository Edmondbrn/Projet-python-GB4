#fichier résumant infos demandées, commenté code, bonus, pimper le code, matrice de contact extraire position atomes

import pretty_errors

import os
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import math

# Constantes
TITLE = "TITLE"
HEADER = "HEADER"
COMPND = "COMPND"
SOURCE = "SOURCE"
KEYWDS = "KEYWDS"
EXPDTA = "EXPDTA"
AUTHOR = "AUTHOR"
JRNL = "JRNL"
RVDAT = "RVDAT"

SEQRES = "SEQRES"
REMARK = "REMARK"

ATOM = "ATOM"

def charger_PDB_fichier(chemin_fichier:str) -> dict[str, list[str]]:
    """Charge un fichier PDB et retourne un dictionnaire tout le fichier organisé par record"""

    if not os.path.exists(chemin_fichier):
        exit(f"Le fichier {chemin_fichier} n'existe pas")

    with open(chemin_fichier, "r") as fichier:
        dico = {}
        for ligne in fichier:
            record_type = ligne[0:6].strip()
            
            if record_type not in dico:
                dico[record_type] = []

            content = ligne[7:80]

            if content:
                dico[record_type].append(content)

    return dico

def charger_PDB_URL(code:str, nom_fichier:str = "temp.pdb") -> dict[str, list[str]]:
    """Charge un fichier PDB à partir d'une URL et retourne un dictionnaire tout le fichier organisé par record"""
    
    url = f"https://files.rcsb.org/download/{code}.pdb"
    try:
        urllib.request.urlretrieve(url, nom_fichier)
        result = charger_PDB_fichier(nom_fichier)
    except Exception as e:
        exit(f"Erreur lors du téléchargement de l'URL: \"{url}\"\n{e}")
    
    if nom_fichier == "temp.pdb":
        os.remove(nom_fichier)

    return result

def get_description(pdb:dict[str, list[str]], include_remarks:bool) -> str:
    """Retourne la description du fichier PDB, incluant les REMARKs si include_remarks est True car les REMARKs peuvent être très longs"""

    description_record_types = [TITLE, HEADER, COMPND, SOURCE, KEYWDS, EXPDTA, AUTHOR, JRNL, RVDAT]
    
    if include_remarks == True: # Est ce que j'ai envie d'inclure les remarques ? Si oui, je les ajoute à la liste des record types à afficher
        description_record_types.append("REMARK")

    separator = "-------------------------------------\n"

    res = ""

    for record_type in description_record_types:
        if record_type in pdb:
            res += separator + record_type + ":\n"
            for record in pdb[record_type]:
                res += record.strip() + "\n"
    
    res += separator
    return res

def get_sequences(pdb:dict[str, list[str]]) -> dict[str: str]:
    """using SEQRES record, return a list of all sequences
    return a dict with chainID as key and sequence as value
    """
    sequences = {}
    debut_chainID, fin_chainID = 4, 5 
    # en adaptant à notre cas, https://www.wwpdb.org/documentation/file-format-content/format33/sect3.html#SEQRES
    # on a 11-12 pour le chainID ==> devient 4, 5

    for sequence_residue in pdb[SEQRES]:
        chainID = sequence_residue[debut_chainID:fin_chainID]

        sequence_line = sequence_residue[12:].strip()

        if chainID not in sequences:
            sequences[chainID] = sequence_line
        else:
            sequences[chainID] += " " + sequence_line
    print(sequences)
    return sequences

def longueur_proteine(pdb:dict[str, list[str]]) -> list[int]:
    res = 0
    for sequence in get_sequences(pdb).values():
        res += len(sequence.split(" "))
    return res

def find_in_record(pdb:dict[str, list[str]], record_type:str, search:str) -> list[str]:
    """return the line of record_type that contains search"""
    res = []
    for record in pdb[record_type]:
        if search in record:
            res.append(record)
    return res

def get_methode_exp(pdb:dict[str, list[str]]) -> str:
    """return method of experiment"""
    # concatenation de toutes les strings de pdb[EXPDATA]
    res = "".join(pdb[EXPDTA]).strip()

    # On suppose que la résolution est toujours dans le REMARK 2 donc on le cherche là
    resolution_search = find_in_record(pdb, REMARK, "2 RESOLUTION.")

    if len(resolution_search) > 0:
        res += "\n" + resolution_search[0][2:]

    return res
        
def ask_for_file() -> str:
    """ask for a PDB file and return the path"""
    while True:
        chemin_fichier = input("Entrez le chemin du fichier PDB: ")
        if os.path.exists(chemin_fichier):
            return chemin_fichier
        else:
            print(f"Le fichier {chemin_fichier} n'existe pas")

def générer_fasta(pdb:dict[str, list[str]]) -> str:
    """génère un fichier fasta à partir d'un fichier PDB"""
    Letters ={
        "ALA":"A",        "ARG":"R",        "ASN":"N",        "ASP":"D",
        "CYS":"C",        "GLN":"Q",        "GLU":"E",        "GLY":"G",
        "HIS":"H",        "ILE":"I",        "LEU":"L",        "LYS":"K",
        "MET":"M",        "PHE":"F",        "PRO":"P",        "SER":"S",
        "THR":"T",        "TRP":"W",        "TYR":"Y",        "VAL":"V",
    }

    sequences = get_sequences(pdb)
    res = ""
    for chainID in sequences:
        res += f">seq{chainID}\n"
        for amino_acid in sequences[chainID].split(" "):
            res += Letters[amino_acid]
        res += "\n"
    return res.strip()

def afficher_ou_enregistrer(string:str, auto_parameter:str = None):
    """affiche ou enregistre le string dans un fichier"""
    if auto_parameter is None:
        choix = input("Voulez-vous afficher le résultat (A) ou l'enregistrer dans un fichier (E) ? ")
    else:
        choix = auto_parameter

    if choix.lower() == "a":
        print(string)
    elif choix.lower() == "e":
        nom_fichier = input("Entrez le nom du fichier: ")
        with open(nom_fichier, "w") as fichier:
            fichier.write(string)
    else:
        print("Choix invalide")

def get_fréquences(acides_aminés:str) -> float:
    compteur_aa={}

    for caractère in acides_aminés:
        if caractère not in compteur_aa:
            compteur_aa[caractère]=1
        else:
            compteur_aa[caractère]+=1
    
    
    return compteur_aa

def comparer_fréquences (fréquence1:dict[str, float], nom_fréquence1:str, fréquence2:dict[str, float], nom_fréquence2:str):
    # use intersection of keys
    keys = []
    for key in fréquence1.keys():
        if key in fréquence2.keys():
            keys.append(key)
    keys.sort()

    # create dataframe
    df = pd.DataFrame(columns=[nom_fréquence1, nom_fréquence2], index=keys)
    for key in keys:
        df.loc[key] = [fréquence1[key], fréquence2[key]]
    
    # plot
    df.plot.bar()
    plt.show()


def calcul_hydrophobicité(acides_aminés:str, taille_fen_glissante:int) -> float:
    hydrophobicite = {
        "A": 0.310, "R": -1.010, "N": -0.600, "D": -0.770,
        "C": 1.540, "Q": -0.220, "E": -0.640, "G": 0.000,
        "H": 0.130, "I": 1.800, "L": 1.700, "K": -0.990,
        "M": 1.230, "F": 1.790, "P": 0.720, "S": -0.040,
        "T": 0.260, "W": 2.250, "Y": 0.960, "V": 1.220
    }

    if not (1 <= taille_fen_glissante <= 9):
        raise ValueError("La taille de la fenêtre glissante doit être entre 1 et 9")

    # Convertir la séquence en une liste d'hydrophobicités
    hydrophobicites = [hydrophobicite[acide] for acide in acides_aminés]

    res = []
    for i in range(len(hydrophobicites)):
        res.append(sum(hydrophobicites[i:i+taille_fen_glissante])/taille_fen_glissante)
    
    return res

def profil_hydrophobicite(hydrophobicite_moyenne:list[float]):
    df = pd.DataFrame(hydrophobicite_moyenne, columns=["Hydrophobicité moyenne"])
    df.plot()
    plt.show()

def split_fasta_sequences(fasta:str) -> dict[str, str]:
    """return a dict with seqID as key and sequence as value"""
    res = {}
    for line in fasta.split("\n"):
        if line.startswith(">"):
            seqID = line[1:]
            res[seqID] = ""
        else:
            res[seqID] += line
    return res

def calcul_distance (coord1:tuple[float, float, float], coord2:tuple[float, float, float]) -> float:
    """calcule la distance entre deux atomes"""
    xa, ya, za = coord1[0], coord1[1], coord1[2]
    xb, yb, zb = coord2[0], coord2[1], coord2[2]

    return math.sqrt(math.pow(xb-xa, 2) 
                     + math.pow(yb-ya, 2) 
                     + math.pow(zb-za, 2)
                     )

def get_cysteines(pdb:dict[str, list[str]]) -> list[str]:
    """Return a list of all ATOM lines that are cysteines"""
    return [atom for atom in pdb['ATOM'] if atom[10:14].strip() == "CYS"]

def détecter_ponts_disulfure(pdb:dict[str, list[str]]) -> list[tuple[str, str]]:
    previous_atom = None
    current_atom = None
    for atom in get_cysteines(pdb):
        atom_name = atom[5:8].strip()
        if atom_name == "SG":
            current_atom = tuple(map(float, atom[24:47].strip().split()))
            if previous_atom is not None:
                distance = calcul_distance(previous_atom, current_atom)
                print("distance ==>", distance)
                if distance < 2.2:
                    print("Pont disulfure détecté !")
                    print(previous_atom, current_atom)
            previous_atom = current_atom
    return []



def main():
    #chemin_fichier = "test.pdb"
    chemin_fichier = "1crn.pdb"
    #chemin_fichier = "12chak.pdb"
    #chemin_fichier = "n'existe pas"

    #chemin_fichier = ask_for_file()

    pdb = charger_PDB_fichier(chemin_fichier)

    #pdb = charger_PDB_URL("1CRN")

    #for record in pdb:
    #    print(record, pdb[record])

    description = get_description(pdb, include_remarks=False)
    print("Description :\n" + description)

    len_protein = longueur_proteine(pdb)
    print("\nLongueur de la proteine :\n" + str(len_protein))

    methode_exp = get_methode_exp(pdb)
    print("\nMethode d'experimentale :\n" + methode_exp)

    fasta = générer_fasta(pdb)
    print("\nFasta :\n" + fasta)

    séquences_fasta = split_fasta_sequences(fasta)
    print("\nSéquences fasta :\n" + str(séquences_fasta))

    premier_fasta = séquences_fasta[list(séquences_fasta.keys())[0]]
    print("\nPremier fasta :\n" + premier_fasta)

    print("\nAffichage ou enregistrement du premier fasta")
    afficher_ou_enregistrer(premier_fasta, auto_parameter="a")

    fréquences = get_fréquences(premier_fasta)
    print("\nFréquences :\n" + str(fréquences))

    swissprot_fréquences = {
        "A": 8.25, "Q": 3.93, "L": 9.65, "S": 6.65,
        "R": 5.53, "E": 6.72, "K": 5.80, "T": 5.36,
        "N": 4.06, "G": 7.07, "M": 2.41, "W": 1.10,
        "D": 5.46, "H": 2.27, "F": 3.86, "Y": 2.92,
        "C": 1.38, "I": 5.91, "P": 4.74, "V": 6.85
    }

    #print("\nComparaison des fréquences avec SwissProt\ncliquez sur la croix pour continuer")
    #comparer_fréquences(fréquences, "PDB", swissprot_fréquences, "SwissProt")

    hydrophobicite_moyenne = calcul_hydrophobicité(premier_fasta, 9)
    print("\nHydrophobicité moyenne :\n" + str(hydrophobicite_moyenne))

    print("\nProfil d'hydrophobicité\ncliquez sur la croix pour continuer")
    profil_hydrophobicite(hydrophobicite_moyenne)

    ponts_disulfure = détecter_ponts_disulfure(pdb)
    

    
if __name__ == "__main__":
    main()



input("Entrez pour fermer")