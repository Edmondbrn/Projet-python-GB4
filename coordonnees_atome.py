#====================================================================================================================

                                        # Importation des modules #

#====================================================================================================================


from Info_imp import FASTA
from math import sqrt




#====================================================================================================================

                                        # Création des fonctions #

#====================================================================================================================


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
