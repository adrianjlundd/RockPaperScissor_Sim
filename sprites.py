from dataclasses import dataclass
from typing import Optional, Tuple
import os
import pygame

from utils import AGENT_RADIUS, IMAGE_FILES, FALLBACK_COLORS


def scale_surface(surface: pygame.Surface, diameter: int) -> pygame.Surface:
	"""Return a copy of the surface scaled to a specific diameter."""
	return pygame.transform.smoothscale(surface, (diameter, diameter)).convert_alpha()


def load_image_or_none(path: str) -> Optional[pygame.Surface]:
	"""Attempt to load an image and return None if it is missing or invalid."""
	if not os.path.isfile(path):
		return None
	try:
		img = pygame.image.load(path).convert_alpha()
		return img
	except Exception:
		return None


def make_circle_surface(color: Tuple[int, int, int], radius: int) -> pygame.Surface:
	"""Create a simple circular fallback sprite with a soft outline."""
	diameter = radius * 2
	surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
	pygame.draw.circle(surf, color, (radius, radius), radius)
	pygame.draw.circle(surf, (0, 0, 0, 100), (radius, radius), radius, 2)  # subtle outline
	return surf


@dataclass
class SpriteSet:
	"""Container for the three rendered sprites used by the agents."""
	rock: pygame.Surface
	paper: pygame.Surface
	scissors: pygame.Surface


def prepare_sprites() -> SpriteSet:
	"""Load PNG sprites from disk and fall back to generated circles if needed."""
	diameter = AGENT_RADIUS * 2
	loaded = {k: load_image_or_none(v) for k, v in IMAGE_FILES.items()}

	if all(loaded.values()):
		rock_img = scale_surface(loaded["rock"], diameter)
		paper_img = scale_surface(loaded["paper"], diameter)
		scissors_img = scale_surface(loaded["scissors"], diameter)
	else:
		rock_img = make_circle_surface(FALLBACK_COLORS["rock"], AGENT_RADIUS)
		paper_img = make_circle_surface(FALLBACK_COLORS["paper"], AGENT_RADIUS)
		scissors_img = make_circle_surface(FALLBACK_COLORS["scissors"], AGENT_RADIUS)

	return SpriteSet(rock=rock_img, paper=paper_img, scissors=scissors_img)


