import txt

import pygame as pg


class boiteTexteRapide:
	"""
	Cette classe permet de créer une surface pour afficher du texte
	"""

	def __init__(self,
				position:tuple,
				tailleFond:tuple,
				couleurFond=(100, 100, 100),
				epaisseurBordure=3,
				couleurBordure=(50, 50, 50),
				texte="",
				couleurTexte=(255, 255, 255),
				texteGras=True,
				police=None,
				taillePolice=24,
				espaceTexteBord=10,
				espaceLigne=5,
				largeurScrollBar=15,
				vitesseScroll=1,
				couleurCurseur=(150, 150, 150)
				) -> None:
		# Informations générales
		self.position = position
		self.tailleFond = tailleFond
		self.rectangle = pg.Rect(0, 0, tailleFond[0], tailleFond[1])

		# Pour préparer le dessin
		self.couleurFond = couleurFond
		self.epaisseurBordure = epaisseurBordure
		self.couleurBordure = couleurBordure

		# Création de la surface du fond
		self.fond = pg.surface.Surface(self.tailleFond)

		# Dessin du fond
		pg.draw.rect(
			self.fond,
			self.couleurFond,
			self.rectangle,
		)

		# Création de la surface de la bordure
		self.bordure = pg.surface.Surface(self.tailleFond)
		self.bordure = self.bordure.convert_alpha()
		self.bordure.fill((0, 0, 0, 0))

		# Dessin de la bordure
		pg.draw.rect(
			self.bordure,
			self.couleurBordure,
			self.rectangle,
			width=self.epaisseurBordure,
		)

		# Création de la surface du fond de la scrollBar
		self.largeurScrollBar = largeurScrollBar
		rectangleScrollBar = (0, 0, largeurScrollBar, self.tailleFond[1])
		self.positionScrollBar = (self.position[0] + self.tailleFond[0], self.position[1])
		self.fondScrollBar = pg.surface.Surface((largeurScrollBar, self.tailleFond[1]))

		# Dessin du fond de scrollBar
		pg.draw.rect(
			self.fondScrollBar,
			self.couleurFond,
			rectangleScrollBar,
		)

		# Variable pour le texte
		self.police = police
		self.texteGras = texteGras
		self.taillePolice = taillePolice
		self.couleurTexte = couleurTexte
		self.espaceLigne = espaceLigne
		self.espaceTexteBord = espaceTexteBord

		policeTexte = pg.font.SysFont(police, taillePolice)
		policeTexte.set_bold(True)
		imageTexte = policeTexte.render("Aj", True, couleurTexte)
		self.hauteurLigne = imageTexte.get_height()

		self.couleurCurseur = couleurCurseur
		self.vitesseScroll = vitesseScroll

		self.changeTexte(texte)


	def changeTexte(self, texte):
		self.debutY = 0

		self.lignes = []
		ligne = ""
		for caractere in texte:
			if caractere != '\n':
				ligne += caractere
			else:
				if caractere != '\n':
					ligne += caractere
				self.lignes.append(ligne)
				ligne = ""

		if len(ligne) > 0:
			self.lignes.append(ligne)

		self.nombreLigne = len(self.lignes)

		self.totalHauteurLigne = (self.hauteurLigne + self.espaceLigne) * (self.nombreLigne - 1)

		# Calcule de la taille du curseur
		self.hauteurMax = self.tailleFond[1] - 2 * self.epaisseurBordure
		if self.totalHauteurLigne != 0:
			self.hauteurCurseur = self.hauteurMax / self.totalHauteurLigne
		else:
			self.hauteurCurseur = self.hauteurMax
		self.hauteurCurseur *= self.hauteurMax
		if self.hauteurCurseur < 1:
			self.hauteurCurseur = 1
		self.hauteurMax -= self.hauteurCurseur
		self.largeurCurseur = self.largeurScrollBar - self.epaisseurBordure

		# Rendu de la boite texte
		self._faireRenduBoiteTexte()


	def _faireRenduBoiteTexte(self):
		# Dessin de la boite texte
		self.dessinBoiteTexte = self.fond.copy()

		positionX = self.espaceTexteBord
		positionY = self.espaceLigne + self.debutY
		i = 0
		while i < self.nombreLigne and positionY < self.tailleFond[1]:
			if positionY >= 0:
				txt.dessinerTexte(self.dessinBoiteTexte, self.lignes[i], (positionX, positionY), self.couleurTexte, self.taillePolice, self.police, self.texteGras)
			positionY += self.hauteurLigne + self.espaceLigne
			i += 1

		self.dessinBoiteTexte.blit(self.bordure, (0, 0))

		# Dessin de la scrollBar
		self.dessinScrollBar = self.fondScrollBar.copy()
		if self.totalHauteurLigne != 0:
			positionY = (self.debutY * -1) / self.totalHauteurLigne
		else:
			positionY = 0
		positionY *= self.hauteurMax
		positionY += self.epaisseurBordure

		pg.draw.rect(
			self.dessinScrollBar,
			self.couleurCurseur,
			(0, positionY, self.largeurCurseur, self.hauteurCurseur))

		pg.draw.line(
			self.dessinScrollBar,
			self.couleurBordure,
			(0, self.epaisseurBordure / 2),
			(self.largeurScrollBar, self.epaisseurBordure / 2),
			self.epaisseurBordure)
		pg.draw.line(
			self.dessinScrollBar,
			self.couleurBordure,
			(0, self.tailleFond[1] - self.epaisseurBordure / 2),
			(self.largeurScrollBar, self.tailleFond[1] - self.epaisseurBordure / 2),
			self.epaisseurBordure)
		pg.draw.line(
			self.dessinScrollBar,
			self.couleurBordure,
			(self.largeurScrollBar - self.epaisseurBordure / 2, 0),
			(self.largeurScrollBar - self.epaisseurBordure / 2, self.tailleFond[1]),
			self.epaisseurBordure)


	def tick(self, positionSourie:tuple[int, int], etatSourie:tuple[bool, bool, bool], scrollSourie:int):
		if positionSourie[0] >= self.position[0] and positionSourie[0] <= self.position[0] + self.tailleFond[0] \
			and positionSourie[1] >= self.position[1] and positionSourie[1] <= self.position[1] + self.tailleFond[1]:

			if scrollSourie < 0:
				self.debutY -= self.hauteurLigne * self.vitesseScroll
				if self.debutY < -self.totalHauteurLigne:
					self.debutY = -self.totalHauteurLigne
				self._faireRenduBoiteTexte()
			if scrollSourie > 0:
				self.debutY += self.hauteurLigne * self.vitesseScroll
				if self.debutY > 0:
					self.debutY = 0
				self._faireRenduBoiteTexte()

		elif positionSourie[0] >= self.position[0] + self.tailleFond[0] and positionSourie[0] <= self.position[0] + self.tailleFond[0] + self.largeurScrollBar\
			and positionSourie[1] >= self.position[1] and positionSourie[1] <= self.position[1] + self.tailleFond[1]:
			if etatSourie[0]:
				sourieY = positionSourie[1] - self.position[1] - self.epaisseurBordure
				sourieY /= self.hauteurMax
				self.debutY = -self.totalHauteurLigne * sourieY
				if self.debutY < -self.totalHauteurLigne:
					self.debutY = -self.totalHauteurLigne
				self._faireRenduBoiteTexte()


	def draw(self, window:pg.surface.Surface):
		window.blit(self.dessinBoiteTexte, self.position)
		window.blit(self.dessinScrollBar, self.positionScrollBar)
