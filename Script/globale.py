###############################################################
#                   Importation des librairies                #
###############################################################
import pygame as pg
import os

###############################################################
#               Définitions des variables globales            #
###############################################################
NOM_FENETRE = "Projet"

# Taille de la fenêtre (largeur, hauteur)
TAILLE_FENETRE = (1800, 1010)

COULEUR_FOND = pg.Color('#000000')

IMAGE_FOND =  pg.image.load("Image retournée2.png")
IMAGE_FOND = pg.transform.scale(IMAGE_FOND, TAILLE_FENETRE)


# Nombre d'image par secondes de l'application
IPS = 30
