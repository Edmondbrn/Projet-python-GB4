#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


# !python3
import urllib.request
import ssl
import os


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


def enregistrement_pdb(chemin, code, PDB):
    """
    Fonction pour enregistrer la fiche PDb dans le dossier contenant les données
    input: chemin du fichier py, le code pdb et la fiche PDB tous au format str
    output: Crée le fichier et retourne le chemin d'accès
    """

    chemin_ss_dossier = chemin + "\\Données\\"+code.upper()
    # Test si le dossier existe déjà ou non
    if not os.path.exists(chemin_ss_dossier):
        #Crée le dossier et change le répertoire de travail
        os.makedirs(chemin_ss_dossier)
        os.chdir(chemin_ss_dossier)
        # Définir le chemin du fichier texte à enregistrer
        fh = open("{}.pdb".format(code.upper()), "w")
        fh.write(PDB)
        fh.close()
    return chemin_ss_dossier


