import os
import sys
import pygame
from typing import Tuple

from utils import (
	WINDOW_WIDTH,
	WINDOW_HEIGHT,
	BACKGROUND_COLOR,
	FPS,
	TITLE_TEXT,
	FONT_NAME,
)
from sprites import prepare_sprites
from simulation import Simulation


def main() -> None:
	"""Entry point: initialize pygame, create the simulation, and run the main loop."""
	pygame.init()
	try:
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	except Exception:
		# Fallback for environments that need explicit flags
		screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED | pygame.RESIZABLE)
	pygame.display.set_caption(TITLE_TEXT)

	clock = pygame.time.Clock()
	font = pygame.font.Font(FONT_NAME, 28)
	small_font = pygame.font.Font(FONT_NAME, 18)

	sprites = prepare_sprites()
	sim = Simulation(screen, sprites, font, small_font)

	running = True
	while running:
		dt_ms = clock.tick(FPS)
		dt = dt_ms / 1000.0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					running = False
				elif event.key == pygame.K_r:
					sim.reset()

		# Update
		sim.update(dt)

		# Draw
		screen.fill(BACKGROUND_COLOR)
		sim.draw()
		sim.draw_hud(fps_value=clock.get_fps())
		pygame.display.flip()

	pygame.quit()
	sys.exit(0)


if __name__ == "__main__":
	main()


