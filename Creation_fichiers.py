#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


from Composition_AA import tableau_bilan_AA
from Info_imp import fusion, info_imp
from coordonnees_atome import pontdisulfure

#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================
def classification(AA, classification, PDB):

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
            nv_B_Factor = classification(AA, Classification, PDB)
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