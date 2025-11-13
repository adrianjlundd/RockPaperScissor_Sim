import math
import os
from typing import Tuple

# -------- Configuration --------
# Window dimensions and appearance
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (24, 24, 24)  # dark gray
FPS = 60  # target frames per second

# Agent movement parameters
NUM_AGENTS_PER_TYPE = 20  # initial population for each species
AGENT_RADIUS = 14
AGENT_MIN_SPEED = 60.0
AGENT_MAX_SPEED = 160.0
AGENT_RANDOM_ACCEL = 40.0  # px/s^2 small jitter for organic motion
COLLISION_COOLDOWN_SEC = 0.35

# UI text configuration
TITLE_TEXT = "Rock Paper Scissors Simulation"
FONT_NAME = None  # default font

# Use images from data/ folder relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGE_FILES = {
	"rock": os.path.join(DATA_DIR, "rock.png"),
	"paper": os.path.join(DATA_DIR, "paper.png"),
	"scissors": os.path.join(DATA_DIR, "scissor.png"),
}

# Fallback colors when PNGs are missing
FALLBACK_COLORS = {
	"rock": (180, 180, 200),      # light gray-blue
	"paper": (200, 230, 200),     # light green
	"scissors": (230, 160, 160),  # light red
}

# RPS rules: who beats who
BEATS = {
	"rock": "scissors",
	"scissors": "paper",
	"paper": "rock",
}


def clamp(value: float, low: float, high: float) -> float:
	"""Clamp the numeric value between the provided lower and upper bounds."""
	return max(low, min(high, value))


def vec_length(x: float, y: float) -> float:
	"""Return the Euclidean length of a 2D vector (x, y)."""
	return math.hypot(x, y)


def normalize(x: float, y: float) -> Tuple[float, float]:
	"""Return a unit vector pointing in the same direction as (x, y)."""
	length = vec_length(x, y)
	if length == 0:
		return 0.0, 0.0
	return x / length, y / length