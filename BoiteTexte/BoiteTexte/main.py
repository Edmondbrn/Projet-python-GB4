import boiteTexte
import texte

#Importation des librairies
import pygame as pg
import sys


class Jeu:
    def __init__(self):
        """
        Cette méthode permet de définir les variables globales du programme
        """
        pg.init() # Initialisation de pygame

        infoObject = pg.display.Info() # On récupère la taille de l'écran
        self.screen_size = ((infoObject.current_w, infoObject.current_h - 63)) # On soustrait la taille de la barre de tâche en bas
        self.screen  = pg.display.set_mode(self.screen_size, pg.RESIZABLE) # On créer la fenêtre

        self.clock = pg.time.Clock() # Permet d'imposer une limite de fps
        self.fps = 60

        self.runJeu = True

        self.couleurFenetre = (150, 150, 150)

        self.boiteTexte = boiteTexte.BoiteTexte(
                            position=(100, 100),
                            tailleFond=(800, 600),
                            texte=texte.texte,
                            police = "monospace".set_bold()
        )


    def run(self):
        """
        Cette méthode permet de définir la boucle principale du jeu
        """
        while self.runJeu: # Boucle pour le jeu
            self.input()
            self.tick()
            self.render()
            self.clock.tick(self.fps)


    def input(self):
        """
        Cette méthode perrmet de gérer les entrées du programme (clic de sourie, appuie de touche)
        """
        self.scrollSourie = 0
        for event in pg.event.get(): # On dit à notre programme de tout arrêter quand on appuie sur la croix en haut à droite
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEWHEEL:
                self.scrollSourie = event.y
        self.etatClavier = pg.key.get_pressed()
        self.etatSourie = pg.mouse.get_pressed()


    def tick(self):
        """
        C'est dans cette méthode que vont s'effectuer tous les calculs des différents éléments de notre programme.
        Par exemple, quand on appuie sur la touche [Flèche gauche], c'est ici qu'on va calculer nle déplacement du joueur
        """
        if self.etatClavier[pg.K_ESCAPE]:
            self.quit()

        self.boiteTexte.tick(pg.mouse.get_pos(), self.etatSourie, self.scrollSourie)


    def render(self): # appel à d'autres fonctions self.render_*() pour l'affichage
        """
        C'est cette méthode qui va gérer l'affichage. Les élements du programme ont déjà bouger, maintenant il ne reste plus qu'à les afficher à l'écran
        """
        self.screen.fill(self.couleurFenetre) # On affiche un écran noir pour effacer tous les autres dessins du précédents passage

        self.boiteTexte.draw(self.screen)

        pg.display.update() # On update, c'est à dire qu'on applique tous les changements précédents à la fenêtre


    def quit(self):
        """
        C'est la méthode, qui va s'executer lorsqu'on veut arrêter le programme
        """
        pg.quit() # On quite pygame
        sys.exit()


Jeu().run() # On lance le jeu
