# ========================================
# SIMULATION CLASS
# ========================================

from world import World
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

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
            "Rock": mpimg.imread("data/rock.png"),
            "Paper": mpimg.imread("data/paper.png"),
            "Scissors": mpimg.imread("data/scissor.png")
        }

        # Choose image zoom size (can be overridden in config)
        self.image_zoom = self.config.get("IMAGE_ZOOM", 0.2)
        self.ax.set_facecolor("#111111")

        # Create an AnnotationBbox artist for each agent and store it so we can
        # update positions every frame. Start visible only if the agent is alive.
        self.agent_artists = []
        for agent in self.world.agents:
            img = OffsetImage(self.images[agent.kind], zoom=self.image_zoom)
            # Use data coordinates for the annotation so xy refers to data
            # coordinates on the axes (this makes updating xy later reliable).
            ab = AnnotationBbox(img, tuple(agent.pos), xycoords='data', frameon=False)
            ab.set_visible(agent.alive)
            self.ax.add_artist(ab)
            self.agent_artists.append(ab)

        
        self.title = self.ax.text(0.02, 1.02, "", transform=self.ax.transAxes)

    def _update_plot(self, frame):
        self.world.update()
        # Update image positions and visibility to follow agents.
        # Try to get renderer for updating AnnotationBbox positions
        # If not available, just update xy and matplotlib will handle it on redraw
        try:
            renderer = self.fig.canvas.get_renderer()
        except AttributeError:
            renderer = None
        
        for agent, artist in zip(self.world.agents, self.agent_artists):
            # Update the annotation position - AnnotationBbox uses .xy for position
            artist.xy = tuple(agent.pos)
            # Update the annotation bbox position using the renderer if available
            if renderer is not None:
                artist.update_positions(renderer)
            
            artist.set_visible(agent.alive)

            # Update image to match agent kind (in case it changed due to
            # interactions). `offsetbox` holds the OffsetImage.
            off = artist.offsetbox
            if off is not None:
                # Update the image data when kind changes
                off.set_data(self.images[agent.kind])

        counts = self.world.count_alive()
        total = sum(counts.values())
        self.title.set_text(
            f"Step {self.world.step_count} — "
            f"Rock:{counts['Rock']} Paper:{counts['Paper']} Scissors:{counts['Scissors']} "
            f"(Total: {total})"
        )

        if self.world.one_species_left():
            self.title.set_text(self.title.get_text() + " — One species left!")
            self.anim.event_source.stop()

        return self.agent_artists,

    def run(self):
        """Start the animation."""
        self.anim = FuncAnimation(
            self.fig, self._update_plot,
            frames=range(self.config["MAX_STEPS"]),
            interval=1, blit=False
        )
        plt.show()