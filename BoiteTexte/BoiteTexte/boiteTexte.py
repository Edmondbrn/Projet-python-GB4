import txt

import pygame as pg


class BoiteTexte:
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
				police=None,
				taillePolice=16,
				espaceTexteBord=10,
				espaceLigne=5,
				largeurScrollBar=15,
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
		self.taillePolice = taillePolice
		self.couleurTexte = couleurTexte
		self.espaceLigne = espaceLigne
		self.espaceTexteBord = espaceTexteBord

		self.debutY = 0

		# Pre-rendu des lignes
		self.lignes = []
		maxLargeurLigne = self.tailleFond[0] + self.epaisseurBordure * 2 - self.espaceTexteBord * 2
		ligne = ""
		for caractere in texte:
			if caractere != '\n':
				ligne += caractere
			else:
				if caractere != '\n':
					ligne += caractere
				renduLigne = txt.surfaceTexte(ligne, self.couleurTexte, self.taillePolice, self.police)
				# La ligne est trop grande
				if renduLigne.get_width() > maxLargeurLigne:
					resteLigne = ligne
					while resteLigne != "":
						ligneDessus = resteLigne
						resteLigne = ""
						renduLigne = txt.surfaceTexte(ligneDessus, self.couleurTexte, self.taillePolice, self.police)
						while renduLigne.get_width() > maxLargeurLigne:
							c = ligneDessus[-1]
							ligneDessus = ligneDessus[:len(ligneDessus) - 1]
							resteLigne = c + resteLigne
							renduLigne = txt.surfaceTexte(ligneDessus, self.couleurTexte, self.taillePolice, self.police)
						self.lignes.append(renduLigne)
				# La ligne est de la bonne taille
				else:
					self.lignes.append(renduLigne)
				ligne = ""

		if len(ligne) > 0:
			self.lignes.append(ligne)

		self.nombreLigne = len(self.lignes)

		self.totalHauteurLigne = 0

		for ligne in self.lignes:
			self.totalHauteurLigne += ligne.get_height() + self.espaceLigne

		self.totalHauteurLigne -= self.lignes[-1].get_height() + self.espaceLigne

		# Calcule de la taille du curseur
		self.hauteurMax = self.tailleFond[1] - 2 * self.epaisseurBordure
		self.hauteurCurseur = self.hauteurMax / self.totalHauteurLigne
		self.hauteurCurseur *= self.hauteurMax
		if self.hauteurCurseur < 1:
			self.hauteurCurseur = 1
		self.hauteurMax -= self.hauteurCurseur
		self.largeurCurseur = self.largeurScrollBar - self.epaisseurBordure
		self.couleurCurseur = couleurCurseur

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
				self.dessinBoiteTexte.blit(self.lignes[i], (positionX, positionY))
			positionY += self.lignes[i].get_height() + self.espaceLigne
			i += 1

		self.dessinBoiteTexte.blit(self.bordure, (0, 0))

		# Dessin de la scrollBar
		self.dessinScrollBar = self.fondScrollBar.copy()
		positionY = (self.debutY * -1) / self.totalHauteurLigne
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
				self.debutY -= 20
				if self.debutY < -self.totalHauteurLigne:
					self.debutY = -self.totalHauteurLigne
				self._faireRenduBoiteTexte()
			if scrollSourie > 0:
				self.debutY += 20
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
