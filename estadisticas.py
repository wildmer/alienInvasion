class Estadisticas():
	"""Seguimiento de las estadísticas de Invasión Alienígena"""

	def __init__(self, ai_configuraciones):
		"""Inicializa las estadísticas"""
		self.ai_configuraciones = ai_configuraciones
		self.reset_stats()

		# Inicia Invasión Alienígena en un estado activo
		self.game_active = False

		# La puntuación alta nunca debe restablecerse
		self.alto_puntaje = 0

	def reset_stats(self):
		"""Inicializa estadísticas que pueden cambiar durante el juego"""
		self.naves_restantes = self.ai_configuraciones.cantidad_naves
		self.puntaje = 0
		self.nivel = 1

	def resetea_puntaje(self):
		"""Resetea el puntaje"""
		self.alto_puntaje = 0
