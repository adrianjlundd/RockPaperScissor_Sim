import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from world import World
from agent import Agent
from simulation import Simulation

# ========================================
# CONFIGURATION
# ========================================

BOX_SIZE = 1.0
SPEED = 0.01
INTERACTION_RADIUS = 0.02
N_AGENTS = 300
FRACTIONS = (0.33, 0.33, 0.34)  # (Rock, Paper, Scissors)
MAX_STEPS = 5000
WRAP = True
SEED = 42

np.random.seed(SEED)




# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
