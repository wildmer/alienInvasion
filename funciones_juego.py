
from time import sleep

import pygame
from bala import Bala

from alien import Alien

def exit_game():
	"""Sale del juego"""
	pygame.quit()
	quit()

def verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas):
	"""Responde a las pulsaciones de teclas"""
	if event.key == pygame.K_RIGHT:
		nave.moving_right = True
	elif event.key == pygame.K_LEFT:
		nave.moving_left = True
	elif event.key == pygame.K_SPACE:
		fuego_bala(ai_configuraciones, pantalla, nave, balas)
	elif event.key == pygame.K_q:
		exit_game()


def verificar_eventos_keyup(event, nave):
	"""Responde a las pulsaciones de teclas"""
	if event.key == pygame.K_RIGHT:
		nave.moving_right = False
	elif event.key == pygame.K_LEFT:
		nave.moving_left = False


def verificar_eventos(ai_configuraciones, pantalla, estadisticas, marcador,
                      play_button, reset_button, exit_button, nave, aliens, balas):
	"""Responde a las pulsaciones de teclas y los eventos del ratón"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit_game()
		elif event.type == pygame.KEYDOWN:
			verificar_eventos_keydown(event, ai_configuraciones, pantalla, nave, balas)

		elif event.type == pygame.KEYUP:
			verificar_eventos_keyup(event, nave)

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_configuraciones, pantalla, estadisticas, marcador,
                            play_button, nave, aliens, balas, mouse_x, mouse_y)
			check_reset_button(ai_configuraciones, pantalla, estadisticas, marcador,
							reset_button, play_button, nave, aliens, balas, mouse_x, mouse_y)
			check_exit_button(ai_configuraciones, pantalla, estadisticas, marcador,
                            exit_button, nave, aliens, balas, mouse_x, mouse_y)


def check_exit_button(ai_configuraciones, pantalla, estadisticas, marcador,
                      exit_button, nave, aliens, balas, mouse_x, mouse_y):
	button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)

	if button_clicked:
		exit_game()
		
def check_play_button(ai_configuraciones, pantalla, estadisticas, marcador,
                      play_button, nave, aliens, balas, mouse_x, mouse_y):
	"""Comienza un nuevo juego cuando el jugador hace clic en Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not estadisticas.game_active:
		# Restablece la configuración del juego
		ai_configuraciones.inicializa_configuraciones_dinamicas()

		# Ocultar el cursor del ratón
		pygame.mouse.set_visible(False)

		# Restablece las estadísticas del juego
		estadisticas.reset_stats()
		estadisticas.game_active = True

		# Restablece las imágenes de marcador
		marcador.prep_puntaje()
		marcador.prep_alto_puntaje()
		marcador.prep_nivel()
		marcador.prep_naves()

		# Vacía la lista de aliens y balas
		aliens.empty()
		balas.empty()

		# Crea una nueva flota y centra la nave
		crear_flota(ai_configuraciones, pantalla, nave, aliens)
		nave.centrar_nave()


def check_reset_button(ai_configuraciones, pantalla, estadisticas, marcador,
                       reset_button, play_button, nave, aliens, balas, mouse_x, mouse_y):
	"""Resetea el juego cuando el jugador hace clic en Reset"""
	button_clicked = reset_button.rect.collidepoint(mouse_x, mouse_y)
	# print(button_clicked)
	if button_clicked:
		estadisticas.resetea_puntaje()
		marcador.prep_alto_puntaje()



def actualizar_pantalla(ai_configuraciones, pantalla, estadisticas,
                        marcador, nave, aliens, balas, play_button, reset_button, exit_button):
	"""Actualiza las imágenes en la pantalla y pasa a la nueva pantalla"""

	# Volver a dibujar la pantalla durante cada pasada por el bucle
	pantalla.fill(ai_configuraciones.bg_color)
	# Vuelve a dibujar todas las balas detrás de la nave y de los extraterrestres
	for bala in balas.sprites():
		bala.draw_bala()
	nave.blitme()
	aliens.draw(pantalla)

	# Dibuja la información de la puntuación
	marcador.muestra_puntaje()

	# Dibuja el botón de Play si el juego está inactivo
	if not estadisticas.game_active:
		play_button.draw_button()
		reset_button.draw_button()
		exit_button.draw_button()

	# Hacer visile la pantalla dibujada más reciente
	pygame.display.flip()


def update_balas(ai_configuraciones, pantalla, estadisticas,
                 marcador, nave, aliens, balas):
	"""Actualiza la posición de las balas y elimina las antiguas"""
	# Actualiza las posiciones de las balas
	balas.update()

	# Deshace las balas que han desaparecido
	for bala in balas.copy():
		if bala.rect.bottom <= 0:
			balas.remove(bala)

	check_bala_alien_collisions(ai_configuraciones, pantalla, estadisticas,
                             marcador, nave, aliens, balas)


def check_bala_alien_collisions(ai_configuraciones, pantalla, estadisticas,
                                marcador, nave, aliens, balas):
	"""Responde a las colisiones entre balas y aliens"""
	# Elimina las balas y los aliens que hayan chocado
	collisions = pygame.sprite.groupcollide(balas, aliens, True, True)

	if collisions:
		for aliens in collisions.values():
			estadisticas.puntaje += ai_configuraciones.puntos_alien * len(aliens)
			marcador.prep_puntaje()
		verifica_alto_puntaje(estadisticas, marcador)

	if len(aliens) == 0:
		# Si se destruye toda la flota, comienza un nuevo nivel
		balas.empty()
		ai_configuraciones.aumentar_velocidad()

		# Incrementa el nivel
		estadisticas.nivel += 1
		marcador.prep_nivel()

		crear_flota(ai_configuraciones, pantalla, nave, aliens)


def verifica_alto_puntaje(estadisticas, marcador):
	"""Verifica si existe un puntaje más alto"""
	if estadisticas.puntaje > estadisticas.alto_puntaje:
		estadisticas.alto_puntaje = estadisticas.puntaje
		marcador.prep_alto_puntaje()


def fuego_bala(ai_configuraciones, pantalla, nave, balas):
	"""Dispara una bala si aún no ha alcanzado el límite"""
	# Crea una nueva bala y la agrega al grupo de balas
	if len(balas) < ai_configuraciones.balas_allowed:
		nueva_bala = Bala(ai_configuraciones, pantalla, nave)
		balas.add(nueva_bala)


def get_number_aliens_x(ai_configuraciones, alien_width):
	"""Determina el número de alienígenas que caben en una fila"""
	available_space_x = ai_configuraciones.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def get_number_rows(ai_configuraciones, nave_height, alien_height):
	"""Determina el número de filas de aliens que se ajustan en la pantalla"""
	available_space_y = (ai_configuraciones.screen_height -
                      (3 * alien_height) - nave_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows


def crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number):
	"""Crea un alien y lo coloca en la fila"""
	alien = Alien(ai_configuraciones, pantalla)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def crear_flota(ai_configuraciones, pantalla, nave, aliens):
	"""Crea una flota completa de alienígenas"""
	# Crea un alien y encuentra el número de aliens seguidos
	# El espacio entre cada alien es igual a un ancho del alien
	alien = Alien(ai_configuraciones, pantalla)
	number_aliens_x = get_number_aliens_x(ai_configuraciones, alien.rect.width)
	number_rows = get_number_rows(
		ai_configuraciones, nave.rect.height, alien.rect.height)

	# Crea la flota de aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			crear_alien(ai_configuraciones, pantalla, aliens, alien_number, row_number)


def check_fleet_edges(ai_configuraciones, aliens):
	"""Responde de forma apropiada si algún alien ha llegado a un borde"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_configuraciones, aliens)
			break


def change_fleet_direction(ai_configuraciones, aliens):
	"""Desciende toda la flota y cambia la dirección de la flota"""
	for alien in aliens.sprites():
		alien.rect.y += ai_configuraciones.fleet_drop_speed
	ai_configuraciones.fleet_direction *= -1


def nave_golpeada(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
	"""Responde a una nave siendo golpeada por un alien"""

	if estadisticas.naves_restantes > 0:
		# Disminuye naves_restantes
		estadisticas.naves_restantes -= 1

		# Actualiza el marcador
		marcador.prep_naves()

		# Vacía la lista de aliens y balas
		aliens.empty()
		balas.empty()

		# Crea una nueva flota y centra la nave
		crear_flota(ai_configuraciones, pantalla, nave, aliens)
		nave.centrar_nave()

	    # Pausa
		sleep(0.5)

	else:
		estadisticas.game_active = False
		pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
	"""Comprueba si algún alien ha llegado al final de la pantalla"""
	pantalla_rect = pantalla.get_rect()

	for alien in aliens.sprites():
		if alien.rect.bottom >= pantalla_rect.bottom:
			# Trata esto de la misma forma que si la nave fuera golpeada
			nave_golpeada(ai_configuraciones, estadisticas,
			              pantalla, marcador, nave, aliens, balas)
			break


def update_aliens(ai_configuraciones, estadisticas, pantalla, marcador, nave, aliens, balas):
	"""Comprueba si la flota está al borde y luego actualiza las posiciones de todos los aliens de la flota"""
	check_fleet_edges(ai_configuraciones, aliens)
	aliens.update()

	# Busca colisiones de alien-nave
	if pygame.sprite.spritecollideany(nave, aliens):
		nave_golpeada(ai_configuraciones, estadisticas,
		              pantalla, marcador, nave, aliens, balas)

	# Busca aliens que golpean la parte inferior de la pantalla
	check_aliens_bottom(ai_configuraciones, estadisticas,
	                    pantalla, marcador, nave, aliens, balas)
