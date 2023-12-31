#IMPORTATION DE MODULE

try:
    import os
    import urllib.request
    from urllib.error import URLError, HTTPError
    import csv
    from math import sqrt
    import ssl

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import tkinter as tk
    import tkinter.messagebox as msg
    from tkinter import Label, Tk, Button, Frame, LabelFrame, Checkbutton, filedialog, StringVar
except:
    input(("problème module"))

#VARIABLE GLOBALE
PDB_fichier=[]
data=[]

#variable définie comme globale  :
#Code_PDB, PDB_fichier, data, fenetre_i, seq, sequence_1Le, atome, sequence_3Le

#------------------
#RECUPERATION DES FICHIERS
#sur internet 
def afficher_input () : 
    #génère la barre d'input 
    code_PDB = tk.Entry(fenetre_i)
    code_PDB.grid(row=8, column=0, columnspan=2)
    #Affiche les instructions supplémentaires
    script_input = "Veuillez saisir le code de la fiche PDB puis appuyer sur Valider."
    l = Label(fenetre_i, text= script_input, font=("Arial",8, "italic"), padx=5, pady=5)
    l.grid(row=7, column=0, columnspan=2, sticky='nsew')
    #Affiche le bouton valider
    valider = tk.Button(fenetre_i, text=" Valider ", command= lambda : loadweb(code_PDB.get()))
    valider.grid(row=9, column=0, columnspan=2 )



def loadweb(codePDB):
    """ Fonction qui permet de charger le contenu d'une fiche PDB d'internet dans une liste,
    input: chaîne de caractères correspondant au codePDB
    output: data = une liste contenant toutes les lignes du codes
            PDB_fichier = une liste contenant pour chaque ligne une liste de mots séparé par un espace"""
    try:
        context = ssl._create_unverified_context() #autorisation pour certain site
        file=urllib.request.urlopen(f"http://files.rcsb.org/view/{codePDB.upper()}.pdb") #,context=context)
        PDB_lines=file.readlines()
        file.close()
        
    except URLError:
        msg_error= ("Le code PDB est introuvable ou nous n'êtes pas connecté à internet. "+ "\n"*2
                    +"Vérifiez le code et votre connexion internet." + "\n"*2 + "Cliquez sur OK puis retapez votre code")
        msg.showerror("Code PDB Error \n", msg_error)
 
    else:
        #récupère le code PDB dans une variable 
        global Code_PDB
        Code_PDB = codePDB
        global PDB_fichier
        global data
        PDB_fichier= []
        data=[]
        for ligne in PDB_lines:
            data.append(ligne.decode("utf8").strip())
            PDB_fichier.append(ligne.decode("utf8").strip())#décode la ligne à partir d'une séquence d'octets en utilisant le jeu de caractères UTF-8 enlève l'espace à la fin
        for i in range(len(data)):
            data[i]=data[i].split() # crée une liste de mot avec comme séparateur un espace => pour chaque ligne tu as les mots séparés
        #on crée une liste avec l'entièreté des lignes du fichier pour conserver le fichier tel quel (plus facile pour récupérer certaines 
        #Ferme la fenêtre d'initialisation
        fenetre_i.destroy()
        #ouvre la fenetre d'exploitation
        app = Application()
        app.mainloop()
        

#en local
def ouvrir_fichier():
    # Ouvrir le gestionnaire de fichiers et obtenir le chemin du fichier sélectionné
    chemin_fichier = filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=[("Fichiers texte", "*.pdb.txt")])  
    nom_fichier = os.path.basename(chemin_fichier)
    dir_path = os.path.dirname(chemin_fichier)
    if dir_path != '' and nom_fichier != '':
        os.chdir(dir_path)
        loadlocal(dir_path, nom_fichier)
    
 
def loadlocal (chemin_fichier, nom_fichier):
    """Fonction recherche une fiche PDB stockée en local pour la stocker dans une liste,
    input: chaîne de caractère correspondante au  chemin d'accès locale du fichier et le nom du fichier
    output: liste contenant toutes les lignes du fichier et une liste contenant pour chaque ligne une liste de mots séparé par un espace"""
    chemin_fichier= os.path.abspath(chemin_fichier) #standardise à partir d'un chemin absolu ou relatif le chemin d'accès à un fichier (=> vérifier pour MAC)
    with open (nom_fichier, 'r') as file : #utilisation de with open permet de fermer en cas d'exception
        PDB_lines=file.readlines()
        global PDB_fichier
        global data
        PDB_fichier= []
        data=[]
    for ligne in PDB_lines:
        data.append(ligne.strip())
        PDB_fichier.append(ligne.strip())
    for i in range(len(data)):
        data[i]=data[i].split() # crée une liste de mot avec comme séparateur un espace => pour chaque ligne tu a les mots séparés
        #récupère le code pbd sans l'extension
        global Code_PDB
        Code_PDB = nom_fichier[:-8] 
        #Ferme la fenêtre d'initialisation
        fenetre_i.destroy()
        #ouvre la fenetre d'exploitation
        app = Application()
        app.mainloop()



#FENETRE D'INITIALISATION
def initialisation(): 
    global fenetre_i
    fenetre_i = Tk()
    label = Label(fenetre_i, text=" Recherche d'informations à partir d'un fichier PDB",fg="blue", font=("Helvetica",12, "bold"), padx=5, pady=5)
    label.grid(row=1, column=0, columnspan=2, sticky='nsew')

    l = LabelFrame(fenetre_i, text="Instructions", padx=5, pady=5)
    l.grid(row=4, column=0, columnspan=2, sticky='nsew')
    script=("Ce programme permet d'extraire des informations d'un fichier PDB et de les visualiser."+ "\n" + 
             "Veuillez choisir le mode d'importation des données de la fiche PDB.")
    label_script = Label(l, text= script)
    label_script.grid(row=5, column=0, columnspan=2, sticky='nsew')

    #en ligne
    enligne = tk.Button(fenetre_i, text=" A partir d'un code PDB ", command=lambda: afficher_input())
    enligne.grid(row=5, column=0, sticky='nsew')

    #en local
    local = tk.Button(fenetre_i, text=" A partir d'une fiche stockée en local", command=lambda: ouvrir_fichier())
    local.grid(row=5, column=1, sticky='nsew')
    
    fenetre_i.mainloop()


#FENETRE D'INITIALISATION
def initialisation_bis(): 
    app = Application()
    app.destroy()
    global fenetre_i
    fenetre_i = Tk()
    label = Label(fenetre_i, text=" Recherche d'informations à partir d'un fichier PDB",fg="blue", font=("Helvetica",12, "bold"), padx=5, pady=5)
    label.grid(row=1, column=0, columnspan=2, sticky='nsew')

    l = LabelFrame(fenetre_i, text="Instructions", padx=5, pady=5)
    l.grid(row=4, column=0, columnspan=2, sticky='nsew')
    script=("Ce programme permet d'extraire des informations d'un fichier PDB et de les visualiser."+ "\n" + 
             "Veuillez choisir le mode d'importation des données de la fiche PDB.")
    label_script = Label(l, text= script)
    label_script.grid(row=5, column=0, columnspan=2, sticky='nsew')

    #en ligne
    enligne = tk.Button(fenetre_i, text=" A partir d'un code PDB ", command=lambda: afficher_input())
    enligne.grid(row=5, column=0, sticky='nsew')

    #en local
    local = tk.Button(fenetre_i, text=" A partir d'une fiche stockée en local", command=lambda: ouvrir_fichier())
    local.grid(row=5, column=1, sticky='nsew')
    
    fenetre_i.mainloop()


#------------
#RECUPERATION DE DONNEES 

def titre (PDB_fichier):
    """Fonction qui récupère le titre du fichier PDB
    input: liste d'élements correpondant à des lignes du fichier PDB
    output: chaîne de caractère contenant le titre du fichier PDB"""
    ligne_titre=PDB_fichier[1]
    titre=ligne_titre[6:]
    return titre

def source(PDB_fichier):
    """Fonction qui récupère l'espèce source de la protéine dans fichier PDB
      input: liste d'élements correpondant à des lignes du fichier PDB
      output: chaine de caractère qui contient le nom de l'espèce source de la protéine"""
    for ligne in PDB_fichier:
        if "SOURCE   2 ORGANISM_SCIENTIFIC" in ligne:
            morceau_source= ligne.split(":")
            source=morceau_source[1]
            return source[:-1]
    return None


def methode(data):
    """Fonction qui récupère la méthode de résolution de la structure protéique dans une fiche PDB
    input: liste de lignes contenant des sous listes de chaques mots d'un fichier PDB
    output: chaine de caractère qui contient le nom de la méthode de résolution de la structure protéique"""
    liste_methode = []
    liste_resolution=[]
    for i in data:
        if i[0] == "EXPDTA":
            liste_methode.append(i[1:])
    methode_resolution = ' '.join([" ".join(line) for line in liste_methode])
    return methode_resolution

def resolution (PDB_fichier):
    """Fonction qui récupère la résolution de la structure protéique dans une fiche PDB
    input: liste de lignes du fichier PDB
    output: chaine de caractère qui contient la valeur de la résolution de la méthode d'analyse de la structure protéique"""
    for ligne in PDB_fichier:
        if "REMARK   2 RESOLUTION" in ligne:
            morceau_resolution= ligne.split(".")
            resolution= morceau_resolution[1]+"."+ morceau_resolution[2]
            return resolution[:-1]
    return "il n'y a pas de résolution pour cette méthode"


#!!!attention il faut trouver comment rechercher la resolution seulement s'il y certaine méthode de resolution!!!


def Calpha (data):
    """Fonction qui récupère les lignes contenant les carbones alpha dans une fiche PDB,
    input: liste de lignes contenant des sous listes de chaques mots d'un fichier PDB
    output: liste des lignes de chaque carbone alpha"""
    Calpha=[]
    for ligne in data:
        if ligne[0]=='ATOM' and 'CA' in ligne:
                Calpha.append(ligne)
    return Calpha

def taille (Calpha):
    """fonction qui donne le nombre d'acides aminés résolus dans la séquence
    input : liste des lignes du fichier PDB correspondantes aux informations des carbones alpha
    output : nombre d'aa résolus"""
    taille_prot=len(Calpha)
    return taille_prot

def analyse_composition(sequence_1L):
    """Fonction qui permet l'analyse de fréquence des acides aminés dans une séquence,
    input: liste de caractères correspondant à la séquence en acides aminés codés avec 1 lettre
    output: dictionnaire où la clé est le code de l'acide aminé à une lettre, et la valeur associée est la fréquence"""
    frequence_moyenne_acides_aminés = {'A': 8.25, 'R': 5.53, 'N': 4.06, 'D': 5.46, 'C': 1.38, 'Q': 3.93, 'E': 6.72, 'G': 7.07, 'H': 2.27, 'I': 5.91,
                                       'L': 9.65, 'K': 5.80, 'M': 2.41, 'F': 3.86, 'P': 4.74, 'S': 6.65, 'T': 5.36, 'W': 1.10, 'Y': 2.92, 'V': 6.85}
    compteur = {aa: 0 for aa in frequence_moyenne_acides_aminés.keys()}  # initialise un dictionnaire pour chaque acide aminé avec une fréquence de 0
    for aa in sequence_1L:
        compteur[aa] += 1  # compte le nombre d'occurrences de chaque acide aminé dans la séquence
    total_aa = sum(compteur.values())  # calcule le nombre total d'acides aminés dans la séquence
    for aa in compteur:
        compteur[aa] = (compteur[aa] / total_aa) * 100  # calcule la fréquence en pourcentage de chaque acide aminé

##    POUR IMPRIMER LA COMPOSITION EN CHAQUE AA
##    for aa in compteur:  # Comparaison avec les fréquences moyennes de la fiche swissprot
##        if aa in frequence_moyenne_acides_aminés:
##            diff = compteur[aa] - frequence_moyenne_acides_aminés[aa]
##            print(f"Pour l'acide aminé {aa}, la fréquence est de {compteur[aa]:.2f}%, ce qui diffère de la fréquence moyenne qui est de {frequence_moyenne_acides_aminés[aa]}% de {diff:.2f}%") #cf internet
    return compteur #diff

def graphique_composition (compteur):
    frequence_moyenne_acides_aminés = {'A': 8.25, 'R': 5.53, 'N': 4.06, 'D': 5.46, 'C': 1.38, 'Q': 3.93, 'E': 6.72, 'G': 7.07, 'H': 2.27, 'I': 5.91,
                                       'L': 9.65, 'K': 5.80, 'M': 2.41, 'F': 3.86, 'P': 4.74, 'S': 6.65, 'T': 5.36, 'W': 1.10, 'Y': 2.92, 'V': 6.85}
    labels = list(compteur.keys()) # Liste des acides aminés
    frequencies = list(compteur.values()) # Liste des fréquences observées
    moyennes = list(frequence_moyenne_acides_aminés.values()) # Liste des fréquences moyennes
    x = np.arange(len(labels)) # Création d'un tableau d'indices pour les étiquettes
    width = 0.3 # Largeur des barres dans le graphique
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, frequencies, width, label='Fréquence observée') # Création des barres pour les fréquences observées
    rects2 = ax.bar(x + width/2, moyennes, width, label='Fréquence moyenne') # Création des barres pour les fréquences moyennes
    ax.set_ylabel('Fréquence en pourcentage')
    ax.set_title('Comparaison des fréquences observées par rapport aux fréquences moyennes')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.show()

def tableau_composition (compteur):
    frequence_moyenne_acides_aminés = {'A': 8.25, 'R': 5.53, 'N': 4.06, 'D': 5.46, 'C': 1.38, 'Q': 3.93, 'E': 6.72, 'G': 7.07, 'H': 2.27, 'I': 5.91,
                                       'L': 9.65, 'K': 5.80, 'M': 2.41, 'F': 3.86, 'P': 4.74, 'S': 6.65, 'T': 5.36, 'W': 1.10, 'Y': 2.92, 'V': 6.85}
    # Création du DataFrame pour le tableau comparatif
    df = pd.DataFrame({'Acide Aminé': list(compteur.keys()), 'Fréquence Observée': list(compteur.values()), 'Fréquence Moyenne': list(frequence_moyenne_acides_aminés.values())})
    return df 

#PAGE DESCRIPTION
def affichage_informations ():
    #Récupération des données
    titre_prot=titre(PDB_fichier)
    global atome
    atome=Calpha (data)
    taille_prot=taille(atome)
    espece= source(PDB_fichier)
    methode_resolution=methode(data)
    valeur_resolution=resolution(PDB_fichier)
    #sequence fasta:
    global sequence_3Le
    sequence_3Le=sequence_3L(atome)
    global sequence_1Le
    sequence_1Le=sequence_1L(sequence_3Le)
    global seq
    seq=sequence_aa(sequence_1Le)
    #pont disulfure:
    dico_soufre=atome_soufre(data)
    liste_distance, liste_positions, liste_souffre_implique=pont_disulfure (dico_soufre)
    liste_non_implique=soufres_non_impliques(dico_soufre, liste_souffre_implique)

    script = ((f"Le titre est{titre_prot}")+ "\n" + (f"Cette protéine provient de l'espèce {espece}.") +"\n" +
              (f"Elle a une taille {taille_prot} acides aminés.")+ "\n"*2 + ("Sa séquence en acides aminés est :")+
              "\n" + seq + "\n"*2 +(f'La méthode de résolution utilisée est {methode_resolution}.')+ "\n" +
              (f'La résolution est de{valeur_resolution}') )
    graphique_composition(Nombre_AA)
    return script              

#PAGE STAT
def affichage_stat():
    #fréquence aa :
    global Nombre_AA
    Nombre_AA= analyse_composition(sequence_1Le)


#-------------
#Création séquence fasta

def sequence_3L (Calpha):
  #"""Fonction qui établie la séquence d'acides aminés d'un fichier PDB avec un code à 3 lettres
  #input: liste des lignes du fichier PDB correspondantes aux informations des carbones alpha
  #output: liste comprenant chaque acide aminé en éléments  """
    sequence_3L=[]
    for aa in Calpha:
        sequence_3L.append(aa[3])
    return sequence_3L


def sequence_1L (sequence_3Lettre):
  #""" Fonction qui traduit une séquence d'acides aminés à 3 lettres en séquence avec le code à 1 lettre
  #input: liste des acides aminés à 3 lettres
  #output: liste des acides aminés à 1 lettre """"
    dico_3L_1L={
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLN': 'Q', 'GLU': 'E',
    'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L','LYS': 'K', 'MET': 'M', 'PHE': 'F',
    'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W','TYR': 'Y','VAL': 'V'}
    sequence_1Lettres=[]
    for i in sequence_3Lettre:
        sequence_1Lettres.append(dico_3L_1L[i])
    return sequence_1Lettres


def sequence_aa(sequence_1Lettre):
    #Fonction qui ajoute un retour à la ligne tous les 80 acides aminés
    #input: liste des acides aminés à 1L
    #output: chaine de caractère avec les acides aminés à 1L et un retour à la ligne tous les 80 caractères
    ligne_aa = ''.join(sequence_1Lettre)
    lines = [ligne_aa[i:i + 80] for i in range(0, len(ligne_aa), 80)]#la 1ère partie crée des segments de 80 aa
    # i prend une valeur qui part de 0 jusqu'à la longeur de séquence avec un incrément de 80
    return '\n'.join(lines)#entre chaque lignes (=segment de 80 aa) on ajoute un retour à la ligne    

#pont disulfure :
def atome_soufre(data):
    #Fonction qui permet d'obtenir les positions des atomes de soufres et leurs coordonnés en plan x,y,z
    #input: une liste contenant toutes les lignes du codes contenant des sous listes pour chaque mots
    #output: dictionnaire avec comme clé le nombre de l'atome dans la séquence et comme valeur les coordonnées en x,y,z
    dico_soufre = {}
    for i in data:
        if i[0] == "ATOM" and i[2] == "SG":
            dico_soufre[i[1]] = [i[6],i[7],i[8]]
    return dico_soufre

def pont_disulfure(dico_soufre):
    """Fonction qui permet d'obtenir les possibles ponts disulfures,
    la distance entre les deux atomes et les soufres impliqués dans un possible ponts disulfures
    input: dictionnaire avec comme clé le nombre de l'atome dans la séquence et comme valeur les coordonnées en x, y, z
    output: 3 listes : liste_distance = contenant les distances entres les atomes qui peuvent être impliqués dans un pont disulfures
    liste_positions=liste des positions des numéros des ponts disulfures qui sont possiblement impliqués dans un pont disulfure
    liste_souffre_implique= liste des soufres qui peuvent êtres impliqué dans un pont disulfure"""

    liste_positions = []
    liste_distance = []
    liste_souffre_implique = []

    # Utiliser une liste pour vérifier l'unicité des cystéines déjà incluses dans un pont disulfure
    cysteines_incluses = []

    for i in dico_soufre:
        for j in dico_soufre:
            if i != j and i not in cysteines_incluses and j not in cysteines_incluses:
                distance = sqrt((float(dico_soufre[i][0]) - float(dico_soufre[j][0]))**2 +
                                (float(dico_soufre[i][1]) - float(dico_soufre[j][1]))**2 +
                                (float(dico_soufre[i][2]) - float(dico_soufre[j][2]))**2)
                if distance <= 3:
                    liste_distance.append(distance)
                    liste_positions.append(i + "-" + j)
                    liste_souffre_implique.append(i)
                    liste_souffre_implique.append(j)

                    # Ajouter les cystéines incluses dans le pont disulfure à l'ensemble
                    cysteines_incluses.append(i)
                    cysteines_incluses.append(j)

    return liste_distance, liste_positions, liste_souffre_implique


def soufres_non_impliques(dico_soufre, liste_souffre_implique):
    #Fonction qui permet d'obtenir la position des soufres qui ne sont pas impliqués dans des ponts disulfures
    #input: dictionnaire avec comme clé le nombre de l'atome dans la séquence et comme valeur les coordonnées en x,y,z et la liste des soufres qui peuvent êtres impliqué dans un pont disulfure
    #output: une liste qui contient la position des
    ensemble_soufres= list(dico_soufre.keys())# on obtient une liste de toutes les positions des soufres
    soufres_non_impliques = [soufre for soufre in ensemble_soufres if soufre not in liste_souffre_implique]
    return soufres_non_impliques

def analyse_composition(sequence_1Lettre): #(SARAH 30/12/23)
    """Fonction qui permet l'analyse de fréquence des acides aminés dans une séquence,
    input: liste de caractères correspondant à la séquence en acides aminés codés avec 1 lettre
    output: dictionnaire où la clé est le code de l'acide aminé à une lettre, et la valeur associée est la fréquence"""
    frequence_moyenne_acides_aminés = {'A': 8.25, 'R': 5.53, 'N': 4.06, 'D': 5.46, 'C': 1.38, 'Q': 3.93, 'E': 6.72, 'G': 7.07, 'H': 2.27, 'I': 5.91,
                                       'L': 9.65, 'K': 5.80, 'M': 2.41, 'F': 3.86, 'P': 4.74, 'S': 6.65, 'T': 5.36, 'W': 1.10, 'Y': 2.92, 'V': 6.85}
    compteur = {aa: 0 for aa in frequence_moyenne_acides_aminés}  # initialise un dictionnaire pour chaque acide aminé avec une fréquence de 0
    for aa in sequence_1Lettre:
        compteur[aa] += 1  # compte le nombre d'occurrences de chaque acide aminé dans la séquence
    total_aa = sum(compteur.values())  # calcule le nombre total d'acides aminés dans la séquence
    for aa in compteur:
        compteur[aa] = (compteur[aa] / total_aa) * 100  # calcule la fréquence en pourcentage de chaque acide aminé
##    for aa in compteur:  # Comparaison avec les fréquences moyennes de la fiche swissprot
##        if aa in frequence_moyenne_acides_aminés:
##            diff = compteur[aa] - frequence_moyenne_acides_aminés[aa]
##            print(f"Pour l'acide aminé {aa}, la fréquence est de {compteur[aa]:.2f}%, ce qui diffère de la fréquence moyenne qui est de {frequence_moyenne_acides_aminés[aa]}% de {diff:.2f}%") #cf internet
    return compteur  #,diff

        
##        for positions, distance in zip(liste_positions, liste_distance):
##            print(f'Un pont disulfure pourrait voir le jour entre les cystéines en positions : {positions} car leur distance est de {distance}')
##        if len(liste_non_implique) != 0:
##            print(f'il existe des soufres qui ne pourraient pas être impliqués dans des ponts disulfures, voici leurs positions: {liste_non_implique}')
##        for aa,frequence in nombre_aa.items():
##            print (f"on retrouve {aa} a une fréquence de {frequence}")

#BONUS
def calcul_distance_calpha(Calpha):
    """Fonction qui calcule la distance entre tous les carbones alpha de la protéine.
    input: liste des lignes contenant les carbones alpha
    output: matrice des distances entre les carbones alpha"""
    coord_calpha = []  # Liste pour stocker les coordonnées des carbones alpha
    for ligne in Calpha: # Extraction des coordonnées des carbones alpha
        if ligne[0] == 'ATOM' and ligne[2] == 'CA':  # Vérifie si la ligne correspond à un atome de carbone alpha
            x = float(ligne[6])
            y = float(ligne[7])
            z = float(ligne[8])
            coord_calpha.append([x, y, z])  # Ajoute les coordonnées à la liste
    n = len(coord_calpha)
    distances = np.zeros((n, n))
    # Calcul de la distance entre les carbones alpha
    for i in range(n): #parcourons des indices des carbones alpha de 0 à n-1 -> sélection carbone alpha de référence
        for j in range(i + 1, n): #parcours des indices des carbones alpha à partir de i+1 jusqu'à n-1 -> sélection carbone alpha distincts de celui de référence
            distance = np.linalg.norm(np.array(coord_calpha[i]) - np.array(coord_calpha[j])) #calcul de la distance entre chaque paire de carbones alpha
            distances[i, j] = distance
            distances[j, i] = distance  # La matrice est symétrique
    return distances

def afficher_matrice_contact(matrice_contact):
    """Affiche la matrice de contact sur un graphique
    input: matrice de contact
    output : graph de la matrice de contact"""
    plt.imshow(matrice_contact, cmap='jet', interpolation='nearest') # Création du graphique de la matrice de contact
    plt.colorbar(label='Distance') # Ajoute une barre de couleur à côté du graphique pour représenter la distance
    plt.title('Matrice de Contact')
    plt.xlabel('Amino acid index')
    plt.ylabel('Amino acid index')
    plt.show()







#FENETRE DE GESTION
class Application(Tk):
    def __init__(self):

        

        Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top")

        
        Button(self.button_frame, text="Description",
                  command=lambda: self.switch_frame(Page_description), height=2, width=12).grid(row=2, column=0, sticky='nsew')
        Button(self.button_frame, text="Statistiques",
                  command=lambda: self.switch_frame(Statistiques), height=2, width=12).grid(row=2, column=1, sticky='nsew')
        Button(self.button_frame, text="Page 3",
                  command=lambda: self.switch_frame(PageThree), height=2, width=12).grid(row=2, column=2, sticky='nsew')
        Button(self.button_frame, text="Bonus",
                  command=lambda: self.switch_frame(Bonus), height=2, width=12).grid(row=2, column=3, sticky='nsew')
        Button(self.button_frame, text=("Nouvelle"+ "\n"+"Recherche"),
                      command=lambda: self.switch_frame(Nouvelle_recherche), height=2, width=12).grid(row=2, column=4, sticky='nsew')
            
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    class StartPage(tk.Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            Label(self, text="Mot de bienvenu").pack(side="top", fill="x", pady=10)

            l = LabelFrame(self, text="Bienvenu à vous cher scientifique ! ", padx=5, pady=5)
            l.pack()
            script_start = (f" Vous allez accéder à une interface contenant les informations contenues dans la fiche PDB {Code_PDB}")
            label_script = Label(l, text= script_start)
            label_script.pack()

    class Page_description(tk.Frame):
        def __init__(self, master):
            Frame.__init__(self, master)
            Label(self, text="Description", fg="blue", font=("Helvetica",12, "bold")).grid(row=1, column=0, sticky='nsew')

            #fenetre header
            d = LabelFrame(self, text="Header", padx=2, pady=5)
            d.grid(row=2, column=0, sticky='nsew')
            Script_d=affichage_informations()
            Label_Script = Label(d, text= Script_d, padx=2, pady=5)
            Label_Script.grid(row=3, column=0, sticky='nsew')

            #fenetre pour enregistrer les données 
            l = LabelFrame(self, text="Gestion de données", padx=2, pady=5)
            l.grid(row=2, column=10, sticky='nsew')
            script_start = ("Cliquez pour enregistrer les informations au format :")
            label_script = Label(l, text= script_start)
            label_script.grid(row=3, column=10, sticky='nsew')
            check_var = tk.IntVar()
            check = tk.Checkbutton(l, text="FASTA", variable=check_var)
            check.grid(row=4, column=10, sticky='nsew')
            button = Button(l, text="Enregistrer", command=lambda: enregistrer_fichier() if check_var.get() else None)
            button.grid(row=5, column=10, sticky='nsew')


class Statistiques(tk.Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Statistiques", fg="blue", font=("Helvetica",12, "bold")).grid(row=1, column=0, sticky='nsew')
        affichage_stat()#défini les variables nécéssaires

        #fenetre séquence 
        s = LabelFrame(self, text="Séquence d'acides aminés", padx=2, pady=5)
        s.grid(row=2, column=0, sticky='nsew')
        Label_Script = Label(s, text= seq, padx=2, pady=5)
        Label_Script.grid(row=3, column=0, sticky='nsew')

        #fenetre tableau
        tab = LabelFrame(self, text="Tableau de fréquence", padx=2, pady=5)
        tab.grid(row=4, column=0, sticky='nsew')
        Script_d=tableau_composition(Nombre_AA)
        Label_Script = Label(tab, text= Script_d, padx=2, pady=5)
        Label_Script.grid(row=5, column=0, sticky='nsew')

        #fenetre graphique
        graph= LabelFrame(self, text="Graphique de fréquence", padx=2, pady=5)
        graph.grid(row=4, column=1, sticky='nsew')
        g=graphique_composition(Nombre_AA)
        Label_Script = Label(graph, text= g, padx=2, pady=5)
        Label_Script.grid(row=5, column=1, sticky='nsew')
            
    
        
class PageThree(tk.Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Page trois", fg="blue", font=("Helvetica",12, "bold")).grid(row=1, column=0, sticky='nsew')

class Bonus(tk.Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Bonus", fg="blue", font=("Helvetica",12, "bold")).grid(row=1, column=0, sticky='nsew')

        CALPHA = Calpha (data)
        matrice_contact = calcul_distance_calpha(CALPHA)
        #fenetre matrice
        mat= LabelFrame(self, text="Matrice de contact", padx=2, pady=5)
        mat.grid(row=2, column=0, sticky='nsew')
        m=afficher_matrice_contact(matrice_contact)
        Label_Script = Label(mat, text= m, padx=2, pady=5)
        Label_Script.grid(row=3, column=0, sticky='nsew')

        
        
class Nouvelle_recherche(tk.Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="Nouvelle Recherche", fg="blue", font=("Helvetica",12, "bold")).grid(row=1, column=0, sticky='nsew')

        #fenetre pour relancer une recherche 
        l = LabelFrame(self, text="Instructions", padx=2, pady=5)
        l.grid(row=2, column=10, sticky='nsew')
        script_start = ("Pour relancer une nouvelle recherche à partir d'un autre code PDB ou d'un autre fichier local, cliquez sur Lancer.")
        label_script = Label(l, text= script_start)
        label_script.grid(row=3, column=0, sticky='nsew')
        button = Button(l, text="Lancer", command=lambda: initialisation_bis())
        button.grid(row=4, column=0, sticky='nsew')



#MAIN
initialisation() 

