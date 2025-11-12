# ========================================
# WORLD CLASS
# ========================================

import numpy as np
from agent import Agent

class World:
    """Holds all agents and handles movement, interactions, and plotting."""

    def __init__(self, config):
        self.config = config
        self.box_size = config["BOX_SIZE"]
        self.wrap = config["WRAP"]
        self.interaction_radius = config["INTERACTION_RADIUS"]
        self.speed = config["SPEED"]
        self.fractions = config["FRACTIONS"]

        n_agents = config["N_AGENTS"]
        self.agents = self._initialize_agents(n_agents)
        self.step_count = 0

    def _initialize_agents(self, n: int):
        """Randomly initialize agents according to FRACTIONS."""
        n_r, n_p, n_s = np.round(np.array(self.fractions) * n).astype(int)
        while n_r + n_p + n_s < n:
            n_r += 1
        kinds = (["Rock"] * n_r) + (["Paper"] * n_p) + (["Scissors"] * n_s)
        np.random.shuffle(kinds)

        positions = np.random.rand(n, 2) * self.box_size
        return [Agent(x, y, kind) for (x, y), kind in zip(positions, kinds)]

    def update(self):
        """Move agents and process interactions."""
        self.step_count += 1
        for agent in self.agents:
            agent.move(self.box_size, self.speed, self.wrap)
        self._process_interactions()

    def _process_interactions(self):
        """Check for collisions and apply RPS elimination."""
        alive_agents = [a for a in self.agents if a.alive]
        n = len(alive_agents)
        if n <= 1:
            return

        for i in range(n):
            a1 = alive_agents[i]
            for j in range(i + 1, n):
                a2 = alive_agents[j]
                if not (a1.alive and a2.alive):
                    continue

                # compute distance (with wrapping)
                diff = a2.pos - a1.pos
                if self.wrap:
                    diff -= np.rint(diff / self.box_size) * self.box_size
                dist = np.hypot(diff[0], diff[1])

                if dist <= self.interaction_radius:
                    if a1.kind == a2.kind:
                        continue
                    elif Agent.beats(a1.kind, a2.kind):
                        a2.alive = False
                    elif Agent.beats(a2.kind, a1.kind):
                        a1.alive = False

    def get_alive_data(self):
        """Return arrays of positions and colors for alive agents."""
        alive = [a for a in self.agents if a.alive]
        if not alive:
            return np.empty((0, 2)), []
        positions = np.array([a.pos for a in alive])
        colors = [a.color() for a in alive]
        kinds = [a.kind for a in alive]
        return positions, colors, kinds

    def count_alive(self):
        """Count remaining agents of each kind."""
        counts = {k: 0 for k in Agent.TYPES}
        for a in self.agents:
            if a.alive:
                counts[a.kind] += 1
        return counts

    def one_species_left(self):
        """Check if only one species remains."""
        alive_types = {a.kind for a in self.agents if a.alive}
        return len(alive_types) <= 1

