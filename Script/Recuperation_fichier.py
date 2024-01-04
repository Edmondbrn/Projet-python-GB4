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
    """
    Fonction pour récupérer la fiche PDB en ligne
    input: code pdb entré par l'utilisateur en str
    output: fiche pdb correspodante en str ou message d'erreur en str
    """
     # Initialisation d'une liste pour stocker les lignes du fichier PDB
    liste_fich = []
    try:
        # Création d'un contexte SSL non vérifié
        context = ssl._create_unverified_context()
         # Ouverture de l'URL en ligne pour obtenir le fichier PDB
        u=urllib.request.urlopen("https://files.rcsb.org/view/"+code.upper()+".pdb", context=context)
        # Lecture des lignes du fichier PDB
        pdblines=u.readlines()
        # fermeture du lien
        u.close()
    except:
        # En cas d'erreur, retourne un message indiquant le problème
        return("Problème lors de la lecture du fichier: \n" + "https://files.rcsb.org/view/"+code.upper()+".pdb\n Veuillez fermer le programme et réessayer")
    else:
         # Si la lecture en ligne est réussie, on convertit les lignes en une seule chaîne de caractères
        for ligne in pdblines:
            #ajoute chaque ligne au format UTF-8 dans la liste, puis les fusionne en une seule chaîne de caractères (fichier) et la retourne.
            liste_fich.append(ligne.decode("utf8").strip() + "\n")
            fichier = "".join(liste_fich)
        return fichier


def importation_locale(code):
    """
    Fonction pour récupérer la fiche PDB en local
    Input: code pdb en str
    Output: fiche pdb en str ou message d'erreur en str
    """
     # Initialisation d'une liste pour stocker les lignes du fichier PDB
    liste_fich = []
    try:
        # Tentative d'ouverture du fichier PDB en mode lecture
        fh = open(code +".pdb", "r")
    except:
         # On retourne un message d'erreur si, par exemple, fichier non trouvé
        return("Le fichier correspondant au code PDB {} n'a pas été trouvé\n Veuillez fermer le programme et réessayer".format(code))
    else:
         # Si l'ouverture du fichier est réussie, on lit chaque ligne et l'ajoute à la liste
        for ligne in fh:
            liste_fich.append(ligne)
        #On ferme le fichier
        fh.close()
        # On fusionne les lignes en une seule chaîne de caractères et la retourne
        Fichier = "".join(liste_fich)
        return Fichier


def enregistrement_pdb(chemin, code, PDB, enregistrement):
    """
    Fonction pour enregistrer la fiche PDB dans le dossier contenant les données
    input: chemin du fichier py, le code pdb et la fiche PDB tous au format str et booléen pour savoir si on doit l'enregistrer ou seulement créer le dossier
    output: Crée le fichier et retourne le chemin d'accès
    """

    chemin_ss_dossier = chemin
    # Test si le dossier existe déjà ou non
    if not os.path.exists(chemin_ss_dossier):
        #Crée le dossier et change le répertoire de travail
        os.makedirs(chemin_ss_dossier)
    if enregistrement:
        # Définir le chemin du fichier texte à enregistrer
        os.chdir(chemin_ss_dossier)
        fh = open("{}.pdb".format(code.upper()), "w")
        fh.write(PDB)
        fh.close()
    return chemin_ss_dossier


