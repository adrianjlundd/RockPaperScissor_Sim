import random
import time
from typing import Dict, List, Optional
import math
import pygame

from utils import (
	NUM_AGENTS_PER_TYPE,
	AGENT_RADIUS,
	AGENT_MIN_SPEED,
	AGENT_MAX_SPEED,
	WINDOW_WIDTH,
	WINDOW_HEIGHT,
	TITLE_TEXT,
)
from sprites import SpriteSet
from agent import Agent


class Simulation:
	"""Manage all agents, run physics, detect winners, and render the HUD."""
	def __init__(self, screen: pygame.Surface, sprites: SpriteSet, font: pygame.font.Font, small_font: pygame.font.Font):
		"""Prepare the simulation with rendering surfaces, fonts, and the initial population."""
		self.screen = screen
		self.sprites = sprites
		self.font = font
		self.small_font = small_font
		self.agents: List[Agent] = []
		self.running = True
		self.paused_for_winner = False
		self.start_time = time.perf_counter()
		self.elapsed_at_win: Optional[float] = None
		self._spawn_initial_agents()

	def _spawn_initial_agents(self) -> None:
		"""Create the starting crowd of rock, paper, and scissors agents."""
		self.agents.clear()
		types_cycle = ["rock", "paper", "scissors"]
		for idx, agent_type in enumerate(types_cycle):
			for _ in range(NUM_AGENTS_PER_TYPE):
				x = random.uniform(AGENT_RADIUS + 2, WINDOW_WIDTH - AGENT_RADIUS - 2)
				y = random.uniform(AGENT_RADIUS + 2, WINDOW_HEIGHT - AGENT_RADIUS - 2)
				angle = random.uniform(0, math.tau)
				speed = random.uniform(AGENT_MIN_SPEED, AGENT_MAX_SPEED)
				vx = math.cos(angle) * speed
				vy = math.sin(angle) * speed
				self.agents.append(Agent((x, y), (vx, vy), agent_type, self.sprites, AGENT_RADIUS))
		self.start_time = time.perf_counter()
		self.paused_for_winner = False
		self.elapsed_at_win = None

	def reset(self) -> None:
		"""Restart the simulation with a fresh set of agents."""
		self._spawn_initial_agents()

	def update(self, dt: float) -> None:
		"""Advance the simulation by dt seconds, resolving movement and battles."""
		if self.paused_for_winner:
			return
		for a in self.agents:
			a.move(dt)
		# Check collisions and resolve fights
		now = time.perf_counter()
		n = len(self.agents)
		for i in range(n):
			for j in range(i + 1, n):
				a = self.agents[i]
				b = self.agents[j]
				if a.collide(b):
					a.fight(b, now)
		# Check winner condition
		counts = self.count_species()
		active_species = [k for k, v in counts.items() if v > 0]
		if len(active_species) == 1:
			self.paused_for_winner = True
			self.elapsed_at_win = time.perf_counter() - self.start_time

	def count_species(self) -> Dict[str, int]:
		"""Return a count of how many agents belong to each species."""
		counts = {"rock": 0, "paper": 0, "scissors": 0}
		for a in self.agents:
			counts[a.type] += 1
		return counts

	def draw_hud(self, fps_value: float) -> None:
		"""Render status information including counts, timer, FPS, and winner banner."""
		# Title centered at top
		title_surf = self.font.render(TITLE_TEXT, True, (230, 230, 240))
		title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 24))
		self.screen.blit(title_surf, title_rect)

		# Counts
		counts = self.count_species()
		count_text = f"Rock: {counts['rock']}   Paper: {counts['paper']}   Scissors: {counts['scissors']}"
		count_surf = self.small_font.render(count_text, True, (220, 220, 220))
		self.screen.blit(count_surf, (16, 52))

		# Elapsed time
		elapsed = (self.elapsed_at_win if self.elapsed_at_win is not None else (time.perf_counter() - self.start_time))
		time_surf = self.small_font.render(f"Time: {elapsed:0.1f}s", True, (200, 200, 200))
		self.screen.blit(time_surf, (16, 76))

		# FPS (optional)
		fps_surf = self.small_font.render(f"FPS: {fps_value:0.1f}", True, (180, 180, 180))
		self.screen.blit(fps_surf, (WINDOW_WIDTH - 120, 12))

		# Winner banner
		if self.paused_for_winner:
			winner = next((k for k, v in counts.items() if v > 0), "None")
			msg = f"{winner.capitalize()} Wins!"
			win_surf = self.font.render(msg, True, (255, 230, 120))
			win_rect = win_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
			self.screen.blit(win_surf, win_rect)

			info_surf = self.small_font.render("Press R to restart", True, (220, 220, 220))
			info_rect = info_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 36))
			self.screen.blit(info_surf, info_rect)

	def draw(self) -> None:
		"""Draw every agent onto the screen surface."""
		for a in self.agents:
			a.draw(self.screen)


