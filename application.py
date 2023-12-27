###############################################################
#                   Importation des librairies                #
###############################################################

import os
# Assignation du chemin d'accès, permet d'éviter les problèmes d'adressage entre les différents systèmes
chemin = __file__
chemin_inv = chemin[::-1]
for i in range(0,len(chemin_inv)):
    #parcourt le chemin d'accès du .py à l'envers jusqu'au premier \\
    if chemin_inv[i]=="\\":
        #Correction de l'emplacement (enlève le nom du fichier .py à la fin du chemin d'accès)
        a = len(chemin)-i
        break
#Sélection du répertoire de travail (celui du fichier .py)   
os.chdir(chemin[:a:])

try:
    from globale import *

    from BoiteTexte.boiteTexteRapide  import boiteTexteRapide
    import pygame as pg
    import pygame_gui as pgg
    import txt
    import pandas as pd
    from Recuperation_fichier import importation_locale, importation_online
    from Info_imp import info_imp, fusion, FASTA
    from Composition_AA import graphique_aa, tableau_bilan_AA
    from Profil_hydrophobicite import graphique_hydro, hydrophobicite
    from coordonnees_atome import pontdisulfure
    from Matrice_contact import graph_matrice, fichier_matrice, matrice_contact
    from Creation_fichiers import fichier_pdb, fichier_bilan

except:
    input("Un problème a eu lieu lors du chargement des modules. Entrer pour fermer et réessayer")
    quit()



###############################################################
#                   Création de la classe                     #
###############################################################
class Application:
    """
    Classe Application
    Gère la fenêtre
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠞⠉⠀⠀⠀⠀⠀⠉⠓⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠑⢲⡄⠀⠀⠀⠀⠀⠀⠀⠈⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⢸⡟⠲⠄⠀⣀⣀⣀⣀⡀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⢸⣧⠀⠀⠀⠀⣿⣏⠀⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⠉⠉⢠⣿⡀⠈⠉⠉⣧⣤⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢆⠀⠀⠸⠛⠇⠀⠀⢠⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠤⠬⢷⠶⡶⠶⠶⢶⡖⣿⣿⣧⠤⠤⢤⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠁⢀⣠⣶⣾⣤⣧⣀⣆⣸⣇⣿⣿⣿⣿⣿⣿⠟⣣⣚⣛⠓⠒⠦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢩⠟⠋⠉⠉⠉⠒⣄⠈⢣⡀⠀⠀⣀⡤⢖⣶⡄
    ⠀⠀⠀⠀⢀⡠⠴⠶⣿⡀⠀⠀⠻⣿⡿⢧⣽⣸⣸⣀⣧⣿⣳⣿⠟⢀⠇⠀⠀⠀⠀⠀⠀⠈⣆⠀⠈⠉⢉⡥⠚⠉⠈⡾
    ⠀⠀⢀⡞⠁⠀⠀⢀⡇⠑⢤⡀⠀⠈⠛⠶⣦⣥⣶⣶⣶⠿⠛⠁⢠⢾⠀⠀⠀⠀⠀⠀⠀⠀⢱⡉⠉⠉⠁⠀⠀⠀⠀⠀
    ⠀⠀⡾⠀⠀⠀⠀⣾⠀⠀⠀⠙⢦⠀⣄⠀⠀⠈⠉⠉⠀⣀⡠⠖⠁⠸⡄⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⢳⠀⠀⠀⠀⣿⠀⠀⠀⠀⠘⡆⢸⠳⣄⣀⢀⡴⠊⠁⠀⠀⠀⠀⠳⣄⡀⠀⠀⠀⣀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠈⣧⡀⠀⠀⠘⣇⠀⠀⠀⠀⠙⢾⣆⠀⠈⠛⠘⢯⠟⠁⠀⠀⠀⡼⠈⣿⠙⠚⢉⣹⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⢠⡯⣉⡶⠒⠒⠛⠢⣀⠀⠀⠀⠀⠈⠁⠀⠀⠼⠶⠖⠂⠀⣠⠞⠁⠀⠈⡏⠉⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⢀⠏⢀⡎⠀⠀⠀⠀⠀⠈⠙⠲⠦⣄⣀⣀⣀⣀⣀⣀⡠⠴⠋⠁⠀⠀⠀⠀⢿⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⡞⢀⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⡀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀  ⢸⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⣇⣼⣀⣠⠤⠤⣤⣀⠤⡄⠀⠀⠀⠀⢸⡉⠉⡏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠘⠿⣿⠯⣭⣍⠭⣷⠏⠀⣸⠦⣄⡀⠀⢸⡇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠓⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠈⠉⠉⠉⠉⣿⣤⣼⠁⠀⠀⣹⣆⢸⠇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⣿⣳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢠⠒⣏⡉⠉⠁⠀⠀⠀⣇⠉⠛⠢⠤⣇⣀⣀⣀⡀⠀⠀⠀⠀⠀⢸⣿⠉⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠘⠷⣄⣉⠉⠉⠐⢀⣴⡇⠙⠲⢤⣀⣀⠀⢈⣉⡇⠀⠀⠀⠀⠀⠸⣿⣄⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⡞⢹⢄⡀⠀⠀⠀⢉⣭⡟⠁⠀⠀⠀⠀⠀⢠⣷⣻⣼⣧⠀⠀⠀⠀⣀⠤⠒⠲⢦⡀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠃⢸⠀⠉⠑⠒⠒⢻⡀⢧⠀⠀⠀⠀⠀⠀⠙⣇⠀⣀⣼⣀⣠⠴⠊⠁⠀⠀⠀⢀⡇⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⡎⠀⠀⠀⠀⠀⠈⢧⠘⡆⠀⠀⠀⠀⠀⠀⠘⢿⠁⠀⠀⠰⡄⠀⠀⠀⣀⡴⠋⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣇⠀⠀⠀⠀⠀⠀⠘⡆⢹⣀⣠⢤⡀⠀⠀⠀⠈⠑⠦⣄⡀⠈⠛⠯⣍⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⠀⣿⣿⢦⠀⠀⠀⠀⢀⣵⠀⣿⠟⠁⢣⠀⠀⠀⠀⠀⠀⠈⠉⠓⠒⠒⠛⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⠹⢿⢿⠤⠟⠁⡞⠀⠀⠀⠰⡟⠛⠉⣀⠴⠋⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠈⡗⠤⠤⠄⠀⠀⡇⠀⠀⠀⠀⠙⢦⠈⢀⡠⠔⠋⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠒⠤⠄⠀⠀⢧⠀⠀⠀⠀⠀⠈⠳⡀⠀⠀⣀⠔⠙⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣒⡶⢦⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠹⡄⠈⠀⠀⡠⠞⠓⠲⠶⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⡴⠊⠉⠁⠀⠀⠈⠉⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠉⢢⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⡟⠀⠀⠀⠀⠀⠀⠀⠀⣠⠤⠚⠁⠀⠀⠀⠀⠀⠀⠀⠈⢧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣷⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠳⣀⣀⣀⣀⣠⠴⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠦⢄⣀⣀⣀⣀⣀⠴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """

    def __init__(self):
        """
        Méthode pour créer nos attributs
        """
        self.fenetre = pg.display.set_mode(TAILLE_FENETRE)
        self.fenetre_texte = pg.display.set_mode(TAILLE_FENETRE)
        self.fond = pg.image.load("Image retournée2.png")

        
        # Défini la page d'origine comme la 1
        self.page = 1
        
        # Appel de nos méthodes pour créer nos pages
        self._creerPage1()
        self._creerPage2()
        self._creerPage3()
        self._creerPage3_bis()
        self._creerPage4()
        self._creerPage5()
        self._creerPage6()
        self._creerPage7()


        
        # Variable pour savoir si l'app est en cours
        self.enCours = False
        
        # Création du timer de l'application
        self.clock = pg.Clock()
        
        # DeltaTime définit le temps d'exécution de la dernière boucle du programme
        self.deltaTime = 0

    
    def _creerPage1(self):
        """
        Méthode pour créer la première page de l'application
        """
        # Création du fond
        self.page1 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page1.fill(COULEUR_FOND)
        self.page1.blit(self.fond, (0,0))

        

        # GUI manager permet de créer des boutons directement
        self.managerPage1 = pgg.UIManager(TAILLE_FENETRE)

        tailleBoutonEntreeTexte = (200, 50)

        # Création de la fenêtre pour rentrer le code PDB de la fiche
        self.entreeTexte = pgg.elements.UITextEntryLine(
                                    relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBoutonEntreeTexte[0] // 2,
                                                            TAILLE_FENETRE[1] // 4),
                                                        tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                    manager=self.managerPage1,
                                    placeholder_text="Nom du fichier"
        )

        # Création de nos boutons
        self.boutonVersPage3 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2.5 - tailleBoutonEntreeTexte[0] // 2,
                                                       TAILLE_FENETRE[1] // 2),
                                                       tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                text="Local",
                                manager=self.managerPage1)
        self.boutonVersPage2 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 1.7 - tailleBoutonEntreeTexte[0] // 2,
                                                       TAILLE_FENETRE[1] // 2),
                                                       tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                text="En ligne",
                                manager=self.managerPage1)

        # Titre de la fenêtre créée en utilisant la fonction drawtext
        taillePolice = 30
        # self.fond = pg.transform.scale(self.fond, TAILLE_FENETRE)
        #                 surface    texte                        position (x, y)
        txt.dessinerTexte(self.page1, "Nom du fichier en ligne", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 4 - (tailleBoutonEntreeTexte[1] // 2)), alignement="haut-centre", couleurTexte=(0,0,0),taillePolice=taillePolice)
        txt.dessinerTexte(self.page1, "Voulez-vous charger une fiche pdb", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 2.5), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)
        txt.dessinerTexte(self.page1, "en local ou en ligne ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 2.5 + taillePolice), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)


    def _creerPage2(self):
        """
        Méthode pour créer la page du chargement en ligne du fichier
        """
        self.page2 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page2.fill(COULEUR_FOND)
        self.page2.blit(self.fond, (0,0))


        # GUI manager permet de créer des boutons directement
        self.managerPage2 = pgg.UIManager(TAILLE_FENETRE)
        
        tailleBouton = (400, 50)
        ecartEntreBouton = 16

        # Création de nos boutons
        self.bouton_enregistrement_fichier_Oui = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] // 2 - (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Télécharger et afficher sur le PC",
                                manager=self.managerPage2)
        self.bouton_enregistrement_fichier_Non = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] // 2 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Uniquement afficher la fiche PDB",
                                manager=self.managerPage2)

        # Titre de la fenêtre créée en utilisant la fonction drawtext
        taillePolice = 30
        txt.dessinerTexte(self.page2, "Voulez-vous uniquement afficher", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)
        txt.dessinerTexte(self.page2, "ou télécharger la fiche PDB ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)


    def _creerPage3(self):
        """
        Méthode pour créer la page du menu
        """
        self.page3 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page2.fill(COULEUR_FOND)
        self.page3.blit(self.fond, (0,0))


        tailleAffichageFichier = (800, 600)

        # GUI manager permet de créer des boutons directement
        self.managerPage3 = pgg.UIManager(TAILLE_FENETRE)

        self.affichageFichier = boiteTexteRapide(
                                    (TAILLE_FENETRE[0] // 4, TAILLE_FENETRE[1] // 8),
                                    tailleAffichageFichier,
                                    police="monospace",
                                    taillePolice=15,
                                    vitesseScroll=4)

        #Création des boutons de la page
        tailleBouton = (200, 50)
        ecartEntreBouton = 16
        # Bouton pour la description générale de la protéine et de la fiche pdb
        self.bouton_analyse_generale = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 1/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Description générale",
                                manager=self.managerPage3)
        
        # Bouton pour afficher la séquence au format FASTA
        self.bouton_sequence_FASTA = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 2/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Séquence FASTA",
                                manager=self.managerPage3)
        
        # Bouton pour l'analyse de l aprésence ou non de pontdisulfure
        self.bouton_Pontdisulfure = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Pontdisulfure",
                                manager=self.managerPage3)
        
        # Bouton pour la modification du fichier .pdb pour le changement de couleurs sur pymol
        self.bouton_modif_Pymol = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 4/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Modif Pymol",
                                manager=self.managerPage3)
        
        #Bouton pour la matrice de contact
        self.bouton_matrice_de_contact = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 5/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Matrice contact",
                                manager=self.managerPage3)
        
        # Bouton pour télécharger le fichier bilan de l'analyse
        self.bouton_analyse_bilan = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 6/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fichier bilan",
                                manager=self.managerPage3)
        
        # Bouton pour afficher la fiche PDB
        self.bouton_fiche_PDB = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] *7/10  + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fiche PDB",
                                manager=self.managerPage3)
        
        self.bouton_nouvelle_fiche = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] *8/10  + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Nouvelle PDB",
                                manager=self.managerPage3)

        taillePolice = 40
        txt.dessinerTexte(self.page3, "Fiche PDB", (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)

    def _creerPage3_bis(self):
        """
        Méthode pour créer la page du menu
        """
        self.page3_bis = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page3_bis.fill(COULEUR_FOND)
        self.page3_bis.blit(self.fond, (0,0))



        # GUI manager permet de créer des boutons directement
        self.managerPage3_bis = pgg.UIManager(TAILLE_FENETRE)

        #Création des boutons de la page
        tailleBouton = (200, 50)
        ecartEntreBouton = 16
        # Bouton pour la description générale de la protéine et de la fiche pdb
        self.retour_page1 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 4/10 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Retour",
                                manager=self.managerPage3_bis)
        
        taillePolice = 30
        txt.dessinerTexte(self.page3_bis, "Un problème a eu lieu lors du chargement de la fiche PDB", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)
        txt.dessinerTexte(self.page3_bis, "Veuillez fermer le programme ou recharger une autre fiche", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", couleurTexte=(0,0,0) ,taillePolice=taillePolice)



    def _creerPage4(self):
        """
        Méthode pour créer la page du choix entre enregistrement ou affichage du la séquence au format FASTA
        """
        self.page4 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page4.fill(COULEUR_FOND)
        self.page4.blit(self.fond, (0,0))

        # GUI manager permet de créer des boutons directement
        self.managerPage4 = pgg.UIManager(TAILLE_FENETRE)

        tailleBouton = (400, 50)
        ecartEntreBouton = 16

        # Création des boutons pour demander si l'utilisateur veut enregistrer ou la non la séquence au format FASTA
        self.bouton_enregistrement_fichierFASTA = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] // 2 - (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Télécharger et afficher sur le PC",
                                manager=self.managerPage4)
        
        self.bouton_affichage_fichierFASTA = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] // 2 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Uniquement afficher la séquence FASTA",
                                manager=self.managerPage4)

        # Titre de la fenêtre créée en utilisant la fonction drawtext
        taillePolice = 30
        txt.dessinerTexte(self.page4, "Voulez-vous uniquement afficher", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)
        txt.dessinerTexte(self.page4, "ou télécharger la séquence au format FASTA ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=taillePolice)


    def _creerPage5(self):
        """
        Méthode pour créer la page d'analyse de la séquence protéique (hydrophobicité et composition en AA)
        """
        self.page5 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page5.fill(COULEUR_FOND)
        self.page5.blit(self.fond, (0,0))


        #tailleAffichageFichier = (800, 600)

        # GUI manager permet de créer des boutons directement
        self.managerPage5 = pgg.UIManager(TAILLE_FENETRE)

        #Création des boutons de la page
        tailleBouton = (200, 50)
        ecartEntreBouton = 16
        # Bouton pour l'analyse de la composition en AA
        self.bouton_analyse_AA = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 2/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Composition en AA",
                                manager=self.managerPage5)
        
        # Bouton pour afficher la séquence au format FASTA
        self.bouton_sequence_hydropobicité = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 4/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Hydrophobicité",
                                manager=self.managerPage5)
        
        self.bouton_retour_menu = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 8/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fiche PDB",
                                manager=self.managerPage5)
        
        self.bouton_sequence_FASTA2 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 6/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Séquence FASTA",
                                manager=self.managerPage5)

        self.taillePolice = 40
        txt.dessinerTexte(self.page5, "Séquence au format FASTA", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", couleurTexte=(0,0,0), taillePolice=20)

       
    def _creerPage6(self):
        """
        Méthode pour créer la page pour que l'utilisateur choisisse comment les AA doivent être colorés sur Pymol
        """
        self.page6 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page6.fill(COULEUR_FOND)
        self.page6.blit(self.fond, (0,0))


        # GUI manager permet de créer des boutons directement
        self.managerPage6 = pgg.UIManager(TAILLE_FENETRE)

        tailleBouton = (200, 50)
        ecartEntreBouton = 16

        self.bouton_Retour = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 5/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fiche PDB",
                                manager=self.managerPage6)

        self.bouton_Frequence = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 3.2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Selon les fréquences",
                                manager=self.managerPage6)
        
        self.bouton_poids = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Selon la masse des AA",
                                manager=self.managerPage6)
        
        self.bouton_polarité = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 1.45 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Selon la polarité",
                                manager=self.managerPage6)




        txt.dessinerTexte(self.page6, "Veuillez choisir votre option" , (TAILLE_FENETRE[0]* 6/12 , TAILLE_FENETRE[1] // 4), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)


    def _creerPage7(self):
        """
        Méthode pour créer la page pour que l'utilisateur choisisse le type de fichier pour recevoir la matrice de contact
        """
        self.page7 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page7.fill(COULEUR_FOND)
        self.page7.blit(self.fond, (0,0))


        # GUI manager permet de créer des boutons directement
        self.managerPage7 = pgg.UIManager(TAILLE_FENETRE)

        tailleBouton = (200, 50)
        ecartEntreBouton = 16

        self.bouton_Retour_matrice = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 5/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fiche PDB",
                                manager=self.managerPage7)

        self.bouton_RDS = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] * 1/5 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fichier .rds",
                                manager=self.managerPage7)
        
        self.bouton_xlsx = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] * 2/5 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fichier .xlsx",
                                manager=self.managerPage7)
        
        self.bouton_csv = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] * 3/5 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fichier .csv",
                                manager=self.managerPage7)
        
        self.bouton_graph_matrice = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] * 4/5 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 3/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Graphique",
                                manager=self.managerPage7)
        
        self.Titre_fenêtre = "Choisissez le type de fichier"
        txt.dessinerTexte(self.page7, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/12 , TAILLE_FENETRE[1] // 4), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)


    def _calculer(self):
        """
        Méthode pour récupérer les changements de l'utilisateur
        et effectuer les changements en fonction de ceux ci
        """
        # On boucle parmi tous les évenements de la fenêtre
        self.scrollSourie = 0
        for event in pg.event.get():
            # Si on a appuyé sur la croix
            if event.type == pg.QUIT:
                self._quit()

            if event.type == pg.MOUSEWHEEL:
                self.scrollSourie = event.y
            
            if event.type == pgg.UI_BUTTON_PRESSED:
                self._gererAppuiBouton(event)
            
            if self.page == 1:
                self.managerPage1.process_events(event)

            elif self.page == 2:
                self.managerPage2.process_events(event)

            elif self.page == 3:
                self.managerPage3.process_events(event)

            elif self.page == "3_bis":
                self.managerPage3_bis.process_events(event)

            elif self.page == 4:
                self.managerPage4.process_events(event)

            elif self.page == 5:
                self.managerPage5.process_events(event)
            
            elif self.page == 6:
                self.managerPage6.process_events(event)

            elif self.page == 7:
                self.managerPage7.process_events(event)

        # On récupère l'état du clavier
        self.etatClavier = pg.key.get_pressed()
        # On récupère l'état de la souris
        self.etatSouris = pg.mouse.get_pressed()
        self.positionSouris = pg.mouse.get_pos()

        # On regarde si la touche Echap est appuyée. Si oui, on quitte l'application
        if self.etatClavier[pg.K_ESCAPE]:
            self._quit()

        if self.page == 1:
            self.managerPage1.update(self.deltaTime)
        if self.page == 2:
            self.managerPage2.update(self.deltaTime)
        if self.page == 3:
            self.managerPage3.update(self.deltaTime)
            self.affichageFichier.tick(self.positionSouris, self.etatSouris, self.scrollSourie)
        if self.page == "3_bis":
            self.managerPage3_bis.update(self.delatTime)
        if self.page == 4:
            self.managerPage4.update(self.deltaTime)
        if self.page == 5:
            self.managerPage5.update(self.deltaTime)
            self.affichageFichier.tick(self.positionSouris, self.etatSouris, self.scrollSourie)
        if self.page == 6:
            self.managerPage6.update(self.deltaTime)
        if self.page == 7:
            self.managerPage7.update(self.deltaTime)
        
        

    def _gererAppuiBouton(self, event):
        if event.ui_element == self.boutonVersPage2:
            self.page = 2

        elif event.ui_element == self.boutonVersPage3:
            
            self.fiche_pdb = importation_locale(self.entreeTexte.text)
            if len(self.fiche_pdb.split("\n")) > 5:
                self.page = 3
                self.affichageFichier.changeTexte(self.fiche_pdb)
            else:
                self.page = "3_bis"
            
        elif event.ui_element == self.retour_page1:
            self.page = 1

        elif event.ui_element == self.bouton_enregistrement_fichier_Oui:
            self.fiche_pdb = importation_online(self.entreeTexte.text)

            if len(self.fiche_pdb.split("\n")) > 5:
                self.page = 3
                self.affichageFichier.changeTexte(self.fiche_pdb)
                fh = open(self.entreeTexte.text+".pdb", "w")
                fh.write(self.fiche_pdb)
                fh.close()
            else:
                self.page = "3_bis"

        
        elif event.ui_element == self.bouton_enregistrement_fichier_Non:
            
            self.fiche_pdb = importation_online(self.entreeTexte.text)
            if len(self.fiche_pdb.split("\n")) > 5:
                self.page = 3
                self.affichageFichier.changeTexte(self.fiche_pdb)
            else:
                self.page = "3_bis"
            
        elif event.ui_element == self.bouton_nouvelle_fiche :
            self.page = 1

        elif event.ui_element == self.bouton_analyse_generale:
            self.description = info_imp(self.fiche_pdb)
            self.affichageFichier.changeTexte(self.description)

        elif event.ui_element == self.bouton_fiche_PDB :
            self.affichageFichier.changeTexte(self.fiche_pdb)

        elif event.ui_element == self.bouton_sequence_FASTA:
            self.page = 4

        elif event.ui_element == self.bouton_enregistrement_fichierFASTA:
            self.page = 5
            self.Titre_fenêtre = "Séquence au format FASTA"
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)



        elif event.ui_element == self.bouton_affichage_fichierFASTA:
            self.page = 5
            self.seq_FASTA = str(fusion(self.fiche_pdb))
            self.texte = self.seq_FASTA
            self.affichageFichier.changeTexte(self.texte)

            self.Titre_fenêtre = "Séquence au format FASTA"
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)


        
        elif event.ui_element == self.bouton_retour_menu:
            self.page = 3

        elif event.ui_element == self.bouton_sequence_hydropobicité:
            # Change le texte dans la tchat box et de la fenêtre
            self.Titre_fenêtre = "Profil d'hydrophobicité"
            self.page5.fill(COULEUR_FOND)
            self.page5.blit(self.fond, (0,0))

            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)

            valeur_hydro = hydrophobicite(self.fiche_pdb)
            self.texte = "Voici les valeurs d'hydrophobicité de la protéine\n*2"
            for i in range(len(valeur_hydro)):
                self.texte += str(i) + "   " + str(round(valeur_hydro[i],3)) + "\n"

            self.affichageFichier.changeTexte(self.texte)
            # Affiche le profil d'hydrophobicité
            graphique_hydro(self.fiche_pdb)


        elif event.ui_element == self.bouton_sequence_FASTA2:
            self.texte = self.seq_FASTA
            self.affichageFichier.changeTexte(self.texte)

            self.Titre_fenêtre = "Séquence au format FASTA"
            self.page5.fill(COULEUR_FOND)
            self.page5.blit(self.fond, (0,0))

            
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre", couleurTexte=(0,0,0), taillePolice=self.taillePolice)

        elif event.ui_element == self.bouton_analyse_AA :
            graphique_aa(self.fiche_pdb)
            self.texte = str(tableau_bilan_AA(self.fiche_pdb))
            self.affichageFichier.changeTexte(self.texte)

            self.Titre_fenêtre = "Analyse composition en acide aminé"
            self.page5.fill(COULEUR_FOND)
            self.page5.blit(self.fond, (0,0))

            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 6/10 , TAILLE_FENETRE[1] // 13), alignement="haut-centre",couleurTexte=(0,0,0),  taillePolice=self.taillePolice)
            
           
        

        elif event.ui_element == self.bouton_modif_Pymol :
            self.page = 6

        elif event.ui_element == self.bouton_Retour :
            self.page = 3

        elif event.ui_element == self.bouton_matrice_de_contact:

            self.page = 7 
            
        elif event.ui_element == self.bouton_graph_matrice:
            self.page = 3
            graph_matrice(self.fiche_pdb)
           

        elif event.ui_element == self.bouton_xlsx:
            self.page = 3
            self.texte_confirmation = fichier_matrice(matrice_contact(self.fiche_pdb), "xlsx", self.entreeTexte.text)
            self.affichageFichier.changeTexte(self.texte_confirmation)

        elif event.ui_element == self.bouton_csv:
            self.page = 3
            self.texte_confirmation = fichier_matrice(matrice_contact(self.fiche_pdb), "csv", self.entreeTexte.text)
            self.affichageFichier.changeTexte(self.texte_confirmation)

        elif event.ui_element == self.bouton_RDS:
            self.page = 3
            self.texte_confirmation = fichier_matrice(matrice_contact(self.fiche_pdb), "rds", self.entreeTexte.text)
            self.affichageFichier.changeTexte(self.texte_confirmation)

        elif event.ui_element == self.bouton_Retour_matrice:
            self.page = 3
        
            
        
        elif event.ui_element == self.bouton_analyse_bilan:
            fichier_bilan(self.fiche_pdb, self.entreeTexte.text)
            self.texte = "Le fichier bilan de {} a bien été créé.".format(self.entreeTexte.text)
            self.affichageFichier.changeTexte(self.texte)
        

        elif event.ui_element == self.bouton_Pontdisulfure:
            self.dico = pontdisulfure(self.fiche_pdb, "SG")
            if type(self.dico) == str :
                 self.affichageFichier.changeTexte(self.dico)
            else:
                self.texte = ""
                self.k = 0
                for element in self.dico:
                    if self.k == 0:
                        self.texte = element + "\n"*2
                        self.k += 1
                        continue

                    elif self.k == 1:
                        self.en_tete = "Il y a un pontdisulfure entre les "
                        
                    else:
                        self.en_tete = "Les cystéines suivantes sont libres  "
                    for donnee in element.keys():
                        self.texte += self.en_tete + donnee + " ("+ str(round(element[donnee], 2))+" A)" + "\n"
                    self.k += 1
                self.affichageFichier.changeTexte(self.texte)

        
        elif event.ui_element == self.bouton_polarité:
            self.page = 3
            self.modif = "polarite"
            self.nom_fichier = self.entreeTexte.text + self.modif
            fichier_pdb(self.fiche_pdb, self.modif, self.nom_fichier)
            self.texte = "Le nouveau fichier pdb a bien été créé"
            self.affichageFichier.changeTexte(self.texte)

        elif event.ui_element == self.bouton_poids:
            self.page = 3
            self.modif = "poids"
            self.nom_fichier = self.entreeTexte.text + self.modif
            fichier_pdb(self.fiche_pdb, self.modif, self.nom_fichier)
            self.texte = "Le nouveau fichier pdb a bien été créé."
            self.affichageFichier.changeTexte(self.texte)
        
        elif event.ui_element == self.bouton_Frequence:
            self.page = 3
            self.modif = "frequence"
            self.nom_fichier = self.entreeTexte.text + self.modif
            fichier_pdb(self.fiche_pdb, self.modif, self.nom_fichier)
            self.texte = "Le nouveau fichier pdb a bien été créé"
            self.affichageFichier.changeTexte(self.texte)



    
    def _dessiner(self):
        """
        Méthode pour dessiner l'application sur la fenêtre
        """
        # On colle le fond à la fenêtre en haut à gauche
        if self.page == 1:
            self.fenetre.blit(self.page1, (0, 0))
            self.managerPage1.draw_ui(self.fenetre)

        elif self.page == 2:
            self.fenetre.blit(self.page2, (0, 0))
            self.managerPage2.draw_ui(self.fenetre)

        elif self.page == 3:
            self.fenetre.blit(self.page3, (0, 0))
            self.managerPage3.draw_ui(self.fenetre)
            self.affichageFichier.draw(self.fenetre)

        elif self.page == "3_bis":
            self.fenetre.blit(self.page3_bis, (0, 0))
            self.managerPage3_bis.draw_ui(self.fenetre)

        elif self.page == 4:
            self.fenetre.blit(self.page4, (0, 0))
            self.managerPage4.draw_ui(self.fenetre)

        elif self.page == 5:
            self.fenetre.blit(self.page5, (0, 0))
            self.managerPage5.draw_ui(self.fenetre)
            self.affichageFichier.draw(self.fenetre)

        elif self.page == 6:
            self.fenetre.blit(self.page6, (0, 0))
            self.managerPage6.draw_ui(self.fenetre)
        
        elif self.page == 7:
            self.fenetre.blit(self.page7, (0, 0))
            self.managerPage7.draw_ui(self.fenetre)

        # On actualise l'affichage de la fenêtre
        pg.display.update()


    def _quit(self):
        """
        Méthode pour quitter l'application
        """
        self.enCours = False


    def lancer(self):
        """
        Méthode pour lancer l'application
        """
        self.enCours = True
        self.page = 1

        while self.enCours:
            self._calculer()
            self._dessiner()
            self.delatTime = self.clock.tick(IPS)

###############################################################
#                   Lancement du programme                    #
###############################################################

# Lancement de pygame
pg.init()


app = Application()

app.lancer()

# On quitte pygame
pg.quit()

