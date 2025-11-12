# ========================================
# AGENT CLASS
# ========================================

import numpy as np

class Agent:
    """Represents a single agent in the RPS world."""

    TYPES = ["Rock", "Paper", "Scissors"]
    COLORS = {"Rock": "#1f77b4", "Paper": "#2ca02c", "Scissors": "#d62728"}

    def __init__(self, x: float, y: float, kind: str):
        self.pos = np.array([x, y], dtype=float)
        self.kind = kind
        self.alive = True

    def move(self, box_size: float, speed: float, wrap: bool):
        """Random movement within the box."""
        if not self.alive:
            return
        angle = np.random.rand() * 2 * np.pi
        self.pos += np.array([np.cos(angle), np.sin(angle)]) * speed

        if wrap:
            self.pos %= box_size
        else:
            self.pos = np.clip(self.pos, 0, box_size)

    def color(self):
        return Agent.COLORS[self.kind]

    @staticmethod
    def beats(a: str, b: str) -> bool:
        """Returns True if type a beats type b according to RPS rules."""
        return (a == "Rock" and b == "Scissors") or \
               (a == "Scissors" and b == "Paper") or \
               (a == "Paper" and b == "Rock")

