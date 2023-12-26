#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


from Info_imp import info_imp
from math import sqrt

import numpy as np
import urllib.request
import ssl
import sys
import platform

#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================


def coordonnees(PDB, atom):
    """Fonction qui extrait les coordonnées dans l'espace d'un atome précis donné
        Input: La fiche PDB au sormat str et l'atome voulu entre SG (soufre des cystéines/ carbone alpha) au format str
        Output: dictionnaire avec en clé l'atome et sa position et en valeur une liste contenant les coordonnées (x,y,z)"""

    if atom == "SG":
        # définit le nom pour le dictionnaire, C = cystéine
        atome = "C"
    else:
        # idem mais pour les carbones alphae = CA
        atome = "CA"
    # Création d'une liste contenant les lignes de la fiche pdb
    PDB = PDB.split("\n")
    # Création des variables pour la boucle while et la taille de la séquence spatialement résolues
    i = 0
    longueur_seq_resolue = 0
    # Ce dictionnaire stockera les coordonnées et l'atoms correspondant
    dico_atome = {}
    # Parcourt de la fiche jusqu'à être dans la partie des coordonées
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
                # Si on a une ligne ANISOU entre les lignes ATOM, on la passe
                else:
                    i += 2
        # Si la ligne ne contient pas CA ou SG, on passe à celle d'après
        else:
            i+=1
    return dico_atome, longueur_seq_resolue


def calcul_distance(PDB, atom):
    """Calcul la distance euclidienne entre 2 atomes donnés
    Input: fiche PDB au format str et l'atome voulu en str
    Output: dictionnaire avec en clé les couples des différents atomes et leurs positions respectives (str) et en valeur la distance entre ces deux
            atomes au format float (3 chiffres après la virgules)"""
    dico_coord,_ = coordonnees(PDB, atom)
    dico_distance = {}
    # Nombre de tours de boucle à sauter
    k = 1
    # Première pour définir l'atome de référence (calcul de distance par rapprot à lui)
    for atome in dico_coord.keys():
        # Récupération de la liste des coordonnées de l'atome
        liste_coord_ref = dico_coord[atome]

        # Stocke le nombre de tours déjà sautés
        y = 0
        # Deuxième boucle pour parcourir tous les autres atomes et uniquement ceux qui n'ont pas été encore étudiés
        for atome_compl in dico_coord.keys():
            # Saute l'atome de référence et les paires d'atomes déjà étudiés
            if y < k :
                y+=1
                continue
            # Calcul des distances
            distance = (float(dico_coord[atome_compl][0]) - float(liste_coord_ref[0]))**2 + (float(dico_coord[atome_compl][1]) - float(liste_coord_ref[1]))**2 + (float(dico_coord[atome_compl][2]) - float(liste_coord_ref[2]))**2
            distance = sqrt(distance)
            # Stockage des distances dans un dictionnaire
            dico_distance[atome + ":" + atome_compl] = distance
        # On passe à un autre atome de référence
        k +=1
    return dico_distance

def recuperation_code_Uniprot(PDB):
    """Récupère le code Uniprot de la protéine de la fiche PDB
    Input: fiche pdb au format str
    Output: le code Uniprot au format str"""
    # Récupération des informations extraites plus tôt
    info_importante = info_imp(PDB)
    info_importante = info_importante.strip()
    info_importante = info_importante.split("\n")
    # Récupération de la dernière ligne
    info_Uniprot = info_importante[-1].split()
    # Récupération du dernier mot, à savoir le code Uniprot
    code_uniprot = info_Uniprot[-1]
    return code_uniprot


def importation_online_uniprot(PDB):
    """Fonction pour récupérer la fiche uniprot en ligne
    Input: fiche PDB en str
    Ouput: fiche uniprot au format str"""
    # Récupération du code et initialisation d ela liste pour stocker la fiche
    code = recuperation_code_Uniprot(PDB)
    liste_fich = []
    # Récupération de la fiche en ligne
    try:
        context = ssl._create_unverified_context()
        u=urllib.request.urlopen("https://rest.uniprot.org/uniprotkb/" + code.upper()+".txt", context=context)
        pdblines=u.readlines()
        u.close()
    except:
        return("Problème lors de la lecture du fichier: \n" + "https://rest.uniprot.org/uniprotkb/"+code.upper()+".txt\n Veuillez fermer le programme et réessayer")
    else:
        # Stockage des lignes dans la liste et transformation de cette liste en str
        for ligne in pdblines:
            liste_fich.append(ligne.decode("utf8").strip() + "\n")
            fichier = "".join(liste_fich)
        return fichier


def secreted(PDB):
    """Vérifie si la protéine est sécrétée
    Input: fiche PDB au format str
    Output: booléen True si la protéine est sécrètée et False dans le cas contraire"""
    # Récupération de la fiche
    uniprot = importation_online_uniprot(PDB)
    uniprot= uniprot.split("\n")
    # Fouille la fiche pour trouver l'annotation de la sécrétion de la protéine
    for ligne in uniprot:
        if "SUBCELLULAR LOCATION: Secreted" in ligne :
            return True
    return False  


def pontdisulfure(PDB, atom):
    """Calcule la présence ou non de pontdisulfure entre les protéines
    Input: fiche pdb en str et atome étudié en str
    Output: 2 dictionnaires respectivement pour les cystéines pontées et non pontées (clé = paire de cystéines, valeur: distance (float))
            et une chaine de caractère pour indiquer si la sécrétion de la protéine a été confirmée ou non
            S'il n'y a pas de cystéines, la fonction renvoie un message sous forme de str"""
    
    # Test si la protéine est sécrétée ou non 
    if secreted(PDB):
        Annonce = "La protéine est sécrétée selon sa fiche Uniprot.\nLes pontdisulfures prédis existent donc bel et bien."
    else:
        Annonce = "La vérification de la sécrétion de la protéine a échoué. \nLes pontdisulfures prédis sont donc hypothétiques."
        # Récupération des données de distance
        dico_distance = calcul_distance(PDB, atom)
        # Si on n'a pas de cystéine dans la séquence
        if dico_distance == {}:
            return "Aucun cystéine n'est présente dans votre séquence"
        # Création des dictionnaires pour les deux types de cystéines
        dico_pontdi = {}
        dico_non_pont = {}
        # Parcourt du dictionnaire contenant les distances entre les paires de cystéines
        for atome in dico_distance.keys():
            # Trie les cystéines selon la distance
            if dico_distance[atome] <= 3:
                dico_pontdi[atome] = dico_distance[atome]
            else:
                dico_non_pont[atome] = dico_distance[atome]
        return Annonce, dico_pontdi, dico_non_pont
