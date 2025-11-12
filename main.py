# ========================================
# MAIN
# ========================================

import numpy as np
from simulation import Simulation

#Global simulation parameters

CONFIG  = {

    "BOX_SIZE": 1.0,
    "SPEED": 0.01,
    "INTERACTION_RADIUS": 0.02,
    "N_AGENTS": 10,
    "FRACTIONS": (0.33, 0.33, 0.34),  # (Rock, Paper, Scissors)
    "MAX_STEPS": 5000,
    "WRAP": True,
    "IMAGE_ZOOM": 0.60,
    

}

np.random.seed(42)  # For reproducibility



if __name__ == "__main__":
    sim = Simulation(CONFIG)
    sim.run()
