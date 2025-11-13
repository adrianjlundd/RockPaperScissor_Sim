import math
import random
import time
from typing import Tuple
import pygame

from utils import (
	AGENT_RADIUS,
	AGENT_MIN_SPEED,
	AGENT_MAX_SPEED,
	AGENT_RANDOM_ACCEL,
	COLLISION_COOLDOWN_SEC,
	WINDOW_WIDTH,
	WINDOW_HEIGHT,
	BEATS,
	normalize,
	vec_length,
	clamp,
)
from sprites import SpriteSet


class Agent:
	"""Autonomous Rock/Paper/Scissors entity that moves, collides, and converts others."""
	def __init__(
		self,
		pos: Tuple[float, float],
		vel: Tuple[float, float],
		agent_type: str,
		sprites: SpriteSet,
		radius: int = AGENT_RADIUS,
	):
		"""Initialize an agent with position, velocity, subtype, and sprite references."""
		self.x, self.y = pos
		self.vx, self.vy = vel
		self.type = agent_type  # 'rock' | 'paper' | 'scissors'
		self.radius = radius
		self.sprites = sprites
		self.image = self._image_for_type(agent_type)
		self.last_collision_time: float = -1e9

	def _image_for_type(self, agent_type: str) -> pygame.Surface:
		"""Return the sprite surface matching the provided agent type."""
		if agent_type == "rock":
			return self.sprites.rock
		if agent_type == "paper":
			return self.sprites.paper
		return self.sprites.scissors

	def set_type(self, agent_type: str) -> None:
		"""Convert this agent to a different type and refresh its sprite."""
		self.type = agent_type
		self.image = self._image_for_type(agent_type)

	def move(self, dt: float) -> None:
		"""Update position and velocity based on random acceleration and wall bounces."""
		# Add gentle random acceleration for organic motion
		ax = random.uniform(-AGENT_RANDOM_ACCEL, AGENT_RANDOM_ACCEL)
		ay = random.uniform(-AGENT_RANDOM_ACCEL, AGENT_RANDOM_ACCEL)
		self.vx += ax * dt
		self.vy += ay * dt

		# Clamp speed
		speed = vec_length(self.vx, self.vy)
		if speed > 0:
			target = clamp(speed, AGENT_MIN_SPEED, AGENT_MAX_SPEED)
			if abs(target - speed) > 1e-3:
				nx, ny = normalize(self.vx, self.vy)
				self.vx = nx * target
				self.vy = ny * target
		else:
			# Give a nudge if stationary
			angle = random.uniform(0, math.tau)
			self.vx = math.cos(angle) * AGENT_MIN_SPEED
			self.vy = math.sin(angle) * AGENT_MIN_SPEED

		# Integrate position
		self.x += self.vx * dt
		self.y += self.vy * dt

		# Bounce off walls
		if self.x - self.radius < 0:
			self.x = self.radius
			self.vx = abs(self.vx)
		elif self.x + self.radius > WINDOW_WIDTH:
			self.x = WINDOW_WIDTH - self.radius
			self.vx = -abs(self.vx)

		if self.y - self.radius < 0:
			self.y = self.radius
			self.vy = abs(self.vy)
		elif self.y + self.radius > WINDOW_HEIGHT:
			self.y = WINDOW_HEIGHT - self.radius
			self.vy = -abs(self.vy)

	def draw(self, screen: pygame.Surface) -> None:
		"""Render the agent's sprite at its current position."""
		rect = self.image.get_rect(center=(int(self.x), int(self.y)))
		screen.blit(self.image, rect)

	def can_collide(self, now: float) -> bool:
		"""Return True if the agent is off cooldown and ready to resolve a collision."""
		return (now - self.last_collision_time) >= COLLISION_COOLDOWN_SEC

	def collide(self, other: "Agent") -> bool:
		"""Check whether this agent overlaps another agent."""
		dx = self.x - other.x
		dy = self.y - other.y
		dist2 = dx * dx + dy * dy
		r = self.radius + other.radius
		return dist2 <= (r * r)

	def fight(self, other: "Agent", now: float) -> None:
		"""Resolve the outcome of a collision and convert the loser to the winner's type."""
		# Avoid repeated immediate collisions
		if not self.can_collide(now) or not other.can_collide(now):
			return
		if self.type == other.type:
			# Gentle separation to reduce sticking for same-type
			self._separate_from(other)
			return
		# Determine winner
		if BEATS[self.type] == other.type:
			# self wins -> convert other
			other.set_type(self.type)
		elif BEATS[other.type] == self.type:
			# other wins -> convert self
			self.set_type(other.type)
		# Cooldown both
		self.last_collision_time = now
		other.last_collision_time = now
		# Small separation to avoid instant re-collide
		self._separate_from(other)

	def _separate_from(self, other: "Agent") -> None:
		"""Push two overlapping agents apart to reduce the chance of rapid re-collision."""
		dx = self.x - other.x
		dy = self.y - other.y
		dist = vec_length(dx, dy)
		if dist == 0:
			angle = random.uniform(0, math.tau)
			dx, dy = math.cos(angle), math.sin(angle)
			dist = 1.0
		nx, ny = dx / dist, dy / dist
		overlap = (self.radius + other.radius) - dist
		if overlap > 0:
			push = overlap / 2.0 + 0.5
			self.x += nx * push
			self.y += ny * push
			other.x -= nx * push
			other.y -= ny * push


