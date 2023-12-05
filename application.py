###############################################################
#                   Importation des librairies                #
###############################################################
from globale import *
import os

import pygame as pg
import pygame_gui as pgg
import txt

import Fonction as F

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

        # Défini la page d'origine comme la 1
        self.page = 1
        
        # Appel de nos méthodes pour créer nos pages
        self._creerPage1()
        self._creerPage2()
        self._creerPage3()
        self._creerPage4()
        self._creerPage5()
        self._creerPage6()


        
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

        # GUI manager permet de créer des boutons directement
        self.managerPage1 = pgg.UIManager(TAILLE_FENETRE)

        tailleBoutonEntreeTexte = (200, 50)

        # Création de la fenêtre pour rentrer le code PDB de la fiche
        self.entreeTexte = pgg.elements.UITextEntryLine(
                                    relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2 - tailleBoutonEntreeTexte[0] // 2,
                                                            TAILLE_FENETRE[1] // 6),
                                                        tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                    manager=self.managerPage1,
                                    placeholder_text="Nom du fichier"
        )

        # Création de nos boutons
        self.boutonVersPage3 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 2.5 - tailleBoutonEntreeTexte[0] // 2,
                                                       TAILLE_FENETRE[1] // 2.5),
                                                       tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                text="Local",
                                manager=self.managerPage1)
        self.boutonVersPage2 = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 1.7 - tailleBoutonEntreeTexte[0] // 2,
                                                       TAILLE_FENETRE[1] // 2.5),
                                                       tailleBoutonEntreeTexte), # (x, y) et (largeur, hauteur)
                                text="En ligne",
                                manager=self.managerPage1)

        # Titre de la fenêtre créée en utilisant la fonction drawtext
        taillePolice = 30
        #                 surface    texte                        position (x, y)
        txt.dessinerTexte(self.page1, "Nom du fichier en ligne", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 6 - (tailleBoutonEntreeTexte[1] // 2)), alignement="haut-centre", taillePolice=taillePolice)
        txt.dessinerTexte(self.page1, "Voulez-vous charger une fiche pdb", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", taillePolice=taillePolice)
        txt.dessinerTexte(self.page1, "en local ou en ligne ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", taillePolice=taillePolice)


    def _creerPage2(self):
        """
        Méthode pour créer la page du chargement en ligne du fichier
        """
        self.page2 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page2.fill(COULEUR_FOND)

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
        txt.dessinerTexte(self.page2, "Voulez-vous uniquement afficher", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", taillePolice=taillePolice)
        txt.dessinerTexte(self.page2, "ou télécharger la fiche PDB ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", taillePolice=taillePolice)


    def _creerPage3(self):
        """
        Méthode pour créer la page du menu
        """
        self.page3 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page3.fill(COULEUR_FOND)

        tailleAffichageFichier = (800, 600)

        # GUI manager permet de créer des boutons directement
        self.managerPage3 = pgg.UIManager(TAILLE_FENETRE)


        self.affichageFichier = pgg.elements.UITextBox(
                                "",
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 3.5,
                                                       TAILLE_FENETRE[1] // 8),
                                                       tailleAffichageFichier), # (x, y) et (largeur, hauteur)
                                manager=self.managerPage3)
        
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
                                text="Fichie PDB",
                                manager=self.managerPage3)
        taillePolice = 40
        txt.dessinerTexte(self.page3, "Fiche PDB", (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=taillePolice)


    def _creerPage4(self):
        """
        Méthode pour créer la page du choix entre enregistrement ou affichage du la séquence au format FASTA
        """
        self.page4 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page4.fill(COULEUR_FOND)
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
        txt.dessinerTexte(self.page4, "Voulez-vous uniquement afficher", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3), alignement="milieu-centre", taillePolice=taillePolice)
        txt.dessinerTexte(self.page4, "ou télécharger la séquence au format FASTA ?", (TAILLE_FENETRE[0] // 2, TAILLE_FENETRE[1] // 3 + taillePolice), alignement="milieu-centre", taillePolice=taillePolice)

    def _creerPage5(self):
        """
        Méthode pour créer la page d'analyse de la séquence protéique (hydrophobicité et composition en AA)
        """
        self.page5 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page5.fill(COULEUR_FOND)

        tailleAffichageFichier = (800, 600)

        # GUI manager permet de créer des boutons directement
        self.managerPage5 = pgg.UIManager(TAILLE_FENETRE)

        # Affichage de la boite de texte pour contenir la séquence
        self.affichageFichierFASTA = pgg.elements.UITextBox(
                                "",
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 3.5,
                                                       TAILLE_FENETRE[1] // 8),
                                                       tailleAffichageFichier), # (x, y) et (largeur, hauteur)
                                manager=self.managerPage5)
        
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
       
    def _creerPage6(self):
        """
        Méthode pour créer la page pour que l'utilisateur choisisse comment les AA doivent être colorés sur Pymol
        """
        self.page6 = pg.Surface(TAILLE_FENETRE)
        # Couleur du fond, marche en RGB aussi (0,0,0)
        self.page6.fill(COULEUR_FOND)

        # GUI manager permet de créer des boutons directement
        self.managerPage6 = pgg.UIManager(TAILLE_FENETRE)

        tailleBouton = (200, 50)
        ecartEntreBouton = 16

        self.bouton_Retour = pgg.elements.UIButton(
                                relative_rect=pg.Rect((TAILLE_FENETRE[0] // 8 - tailleBouton[0] // 2,
                                                       TAILLE_FENETRE[1] * 5/12 + (tailleBouton[1] // 2 + ecartEntreBouton // 2)),
                                                       tailleBouton), # (x, y) et (largeur, hauteur)
                                text="Fiche PDB",
                                manager=self.managerPage6)

        txt.dessinerTexte(self.page6, "Veuillez choisir votre option" , (TAILLE_FENETRE[0]* 6/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)



   

    def _calculer(self):
        """
        Méthode pour récupérer les changements de l'utilisateur
        et effectuer les changements en fonction de ceux ci
        """
        # On boucle parmi tous les évenements de la fenêtre
        for event in pg.event.get():
            # Si on a appuyé sur la croix
            if event.type == pg.QUIT:
                self._quit()
            
            if event.type == pgg.UI_BUTTON_PRESSED:
                self._gererAppuiBouton(event)
            
            if self.page == 1:
                self.managerPage1.process_events(event)

            elif self.page == 2:
                self.managerPage2.process_events(event)

            elif self.page == 3:
                self.managerPage3.process_events(event)

            elif self.page == 4:
                self.managerPage4.process_events(event)

            elif self.page == 5:
                self.managerPage5.process_events(event)
            
            elif self.page == 6:
                self.managerPage6.process_events(event)

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
        if self.page == 4:
            self.managerPage4.update(self.deltaTime)
        if self.page == 5:
            self.managerPage5.update(self.deltaTime)
        if self.page == 6:
            self.managerPage6.update(self.deltaTime)
        

    def _gererAppuiBouton(self, event):
        if event.ui_element == self.boutonVersPage2:
            self.page = 2

        elif event.ui_element == self.boutonVersPage3:
            self.page = 3
            self.fiche_pdb = F.importation_locale(self.entreeTexte.text)

            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{0}</font><br>'.format(self.fiche_pdb))



        elif event.ui_element == self.bouton_enregistrement_fichier_Oui:
            self.page = 3
            self.fiche_pdb = F.importation_online(self.entreeTexte.text)


            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{0}</font><br>'.format(self.fiche_pdb))

            fh = open(self.entreeTexte.text+".pdb", "w")
            fh.write(self.fiche_pdb)
            fh.close()
        
        elif event.ui_element == self.bouton_enregistrement_fichier_Non:
            self.page = 3
            self.fiche_pdb = F.importation_online(self.entreeTexte.text)

            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{0}</font><br>'.format(self.fiche_pdb))

        elif event.ui_element == self.bouton_analyse_generale:

            self.description = F.info_imp(F.importation_online(self.entreeTexte.text))
            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.description))

        elif event.ui_element == self.bouton_fiche_PDB :
            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.fiche_pdb))



        elif event.ui_element == self.bouton_sequence_FASTA:
            self.page = 4

        elif event.ui_element == self.bouton_enregistrement_fichierFASTA:
            self.page = 5
            self.Titre_fenêtre = "Séquence au format FASTA"
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)



        elif event.ui_element == self.bouton_affichage_fichierFASTA:
            self.page = 5
            self.texte = str(F.fusion(self.fiche_pdb))
            self.affichageFichierFASTA.set_text(f'<font face=arial size=4 color=#FFFFFF>{self.texte}</font><br>')

            self.Titre_fenêtre = "Séquence au format FASTA"
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)


        
        elif event.ui_element == self.bouton_retour_menu:
            self.page = 3

        elif event.ui_element == self.bouton_sequence_hydropobicité:
            # Change le texte dans la tchat box
            self.texte = "Profil hydrophobicité"
            self.affichageFichierFASTA.set_text(f'<font face=arial size=4 color=#FFFFFF>{self.texte}</font><br>')
            self.Titre_fenêtre = "Profil d'hydrophobicité"

            # Change le titre de la page
            self.page5.fill(COULEUR_FOND)
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)

        elif event.ui_element == self.bouton_sequence_FASTA2:
            self.texte = F.fusion(self.fiche_pdb)
            self.affichageFichierFASTA.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.texte))

            self.Titre_fenêtre = "Séquence FASTA"
            self.page5.fill(COULEUR_FOND)
            
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)

          
        elif event.ui_element == self.bouton_analyse_AA :
            self.texte = str(F.tableau_bilan_AA(self.fiche_pdb))
            self.affichageFichierFASTA.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.texte))

            self.Titre_fenêtre = "Analyse composition en acide aminé"
            self.page5.fill(COULEUR_FOND)
            txt.dessinerTexte(self.page5, self.Titre_fenêtre , (TAILLE_FENETRE[0]* 7/12 , TAILLE_FENETRE[1] // 20), alignement="haut-centre", taillePolice=self.taillePolice)
            F.graphique_aa(self.fiche_pdb)

        elif event.ui_element == self.bouton_modif_Pymol :
            self.page = 6


        elif event.ui_element == self.bouton_Retour :
            self.page = 3

        elif event.ui_element == self.bouton_matrice_de_contact:
            F.graph_matrice(self.fiche_pdb)
            self.matrice = F.matrice_contact(self.fiche_pdb)
            self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.matrice))

        elif event.ui_element == self.bouton_Pontdisulfure:
            self.dico = F.pontdisulfure(self.fiche_pdb, "SG")
            if type(self.dico) == str :
                 self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.dico))
            else:
                self.texte = ""
                self.k = 0
                for element in self.dico:
                    if self.k == 0:
                        self.en_tete = "Il y a un pontdisulfure entre les "
                    else:
                        self.en_tete = "Les cystéines suivantes sont libres  "
                    for donnee in element.keys():
                        self.texte += self.en_tete + donnee + " ("+str(round(element[donnee], 2))+" A)" + "\n"
                    self.k += 1
                self.affichageFichier.set_text('<font face=arial size=4 color=#FFFFFF>{}</font><br>'.format(self.texte))

            
    
    
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

        elif self.page == 4:
            self.fenetre.blit(self.page4, (0, 0))
            self.managerPage4.draw_ui(self.fenetre)

        elif self.page == 5:
            self.fenetre.blit(self.page5, (0, 0))
            self.managerPage5.draw_ui(self.fenetre)

        elif self.page == 6:
            self.fenetre.blit(self.page6, (0, 0))
            self.managerPage6.draw_ui(self.fenetre)
        
        
        

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

