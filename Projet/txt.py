import pygame as pg
import tkinter as tk
from tkinter import scrolledtext
import sys
from globale import *
import urllib.request
import ssl
import sys
import platform
import Fonction as charge

def dessinerTexte(surface, texte, position, couleurTexte=(255, 255, 255), taillePolice=24, policeTexte=None, alignement="haut-gauche"):
	policeTexte = pg.font.SysFont(policeTexte, taillePolice)
	imageTexte = policeTexte.render(texte, True, couleurTexte)

	placement = position
	
	if alignement == "milieu-gauche":
		placement = (position[0], position[1] - imageTexte.get_height() / 2)
	elif alignement == "bas-gauche":
		placement = (position[0], position[1] - imageTexte.get_height())

	elif alignement == "haut-centre":
		placement = (position[0] - imageTexte.get_width() / 2, position[1])
	elif alignement == "milieu-centre":
		placement = (position[0] - imageTexte.get_width() / 2, position[1] - imageTexte.get_height() / 2)
	elif alignement == "bas-centre":
		placement = (position[0] - imageTexte.get_width() / 2, position[1] - imageTexte.get_height())

	elif alignement == "haut-droite":
		placement = (position[0] - imageTexte.get_width(), position[1])
	elif alignement == "milieu-droite":
		placement = (position[0] - imageTexte.get_width(), position[1] - imageTexte.get_height() / 2)
	elif alignement == "bas-droite":
		placement = (position[0] - imageTexte.get_width(), position[1] - imageTexte.get_height())
	
	return surface.blit(imageTexte, placement)


# def Affiche_PDB(texte):
# 	Fenetre_PDB = tk.Tk()
# 	Fenetre_PDB.title("Fenêtre avec Texte")

# 	# Zone de texte avec défilement
# 	fenetre_texte = tk.scrolledtext.ScrolledText(Fenetre_PDB, width=40, height=10, wrap=tk.WORD)
# 	fenetre_texte.insert(tk.END, texte)
# 	fenetre_texte.pack(expand=True, fill='both')
# 	pg.display.update()
# 	Fenetre_PDB.mainloop()
