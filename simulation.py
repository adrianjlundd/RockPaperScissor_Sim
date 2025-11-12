# ========================================
# SIMULATION CLASS
# ========================================

from world import World
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlix.image as mpimg

class Simulation:
   
    """Runs and visualizes the RPS world simulation."""

    def __init__(self, config):
        self.config = config
        self.world = World(config)

        # Set up plotting
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.set_xlim(0, self.config["BOX_SIZE"])
        self.ax.set_ylim(0, self.config["BOX_SIZE"])
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.images = {
            "Rock": mpimg.imread("images/rock.png"),
            "Paper": mpimg.imread("images/paper.png"),
            "Scissors": mpimg.imread("images/scissors.png")
        }

        # Store artists objects for each agent
        self.agent_artists = []
        for agent in self.world.agents:
            img = OffsetImage(self.images[agent.kind], zoom=0.05)
            ab = AnnotationBbox(img, agent.pos, frameon=False)
            self.ax.add_artist(ab)
            self.agent_artists.append(ab)

        
        self.title = self.ax.text(0.02, 1.02, "", transform=self.ax.transAxes)

    def _update_plot(self, frame):
        self.world.update()
        positions, colors, kinds = self.world.get_alive_data()
        self.scatter.set_offsets(positions)
        self.scatter.set_facecolor(colors)
        self.scatter.set_edgecolor("k")

        counts = self.world.count_alive()
        self.title.set_text(
            f"Step {self.world.step_count} — "
            f"R:{counts['Rock']} P:{counts['Paper']} S:{counts['Scissors']}"
        )

        if self.world.one_species_left():
            self.title.set_text(self.title.get_text() + " — One species left!")
            self.anim.event_source.stop()

        return self.scatter,

    def run(self):
        """Start the animation."""
        self.anim = FuncAnimation(
            self.fig, self._update_plot,
            frames=range(self.config["MAX_STEPS"]),
            interval=1, blit=False
        )
        plt.show()