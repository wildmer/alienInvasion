import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""Sirve para representar a un solo alienígena en la flota"""

	def __init__(self, ai_configuraciones, pantalla):
		"""Inicializa el alien y establece su posición inicial"""
		super(Alien, self).__init__()

		self.pantalla = pantalla
		self.ai_configuraciones = ai_configuraciones

		# Carga la imagen del alien y establece su atributo rect
		self.image = pygame.image.load("imagenes/ovnii.png")
		self.rect = self.image.get_rect()

		# Inicia cada nuevo alien cerca de la parte superior izquierda de la pantalla
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Almacena la posición exacta del alien
		self.x = float(self.rect.x)

	def blitme(self):
		"""Dibuja el alien en su ubicación actual"""
		self.pantalla.blit(self.image, self.rect)

	def check_edges(self):
		"""Devuelve Verdadero si el alien está en el borde de la pantalla"""
		screen_rect = self.pantalla.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		"""Mueve el alien a la derecha"""
		# self.x += (self.ai_configuraciones.alien_speed_factor *
		# self.ai_configuraciones.fleet_direction)
		self.x += (self.ai_configuraciones.alien_speed_factor *
                    self.ai_configuraciones.fleet_direction)
		self.rect.x = self.x
