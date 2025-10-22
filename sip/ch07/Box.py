import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ****************************************
# Box Class
# ****************************************
class Box:
    """
    Box contains data for particles in a partitioned box.
    """
    def __init__(self, N):
        """
        Initializes the box with N particles.
        
        :param N: The number of particles.
        """
        self.N = N
        self.x = np.zeros(N)
        self.y = np.zeros(N)
        self.nleft = 0
        self.time = 0
        self.initialize()

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def initialize(self):
        """
        Initializes the box, places particles in random positions on the left side.
        """
        self.nleft = self.N  # Start with all particles on the left
        self.time = 0
        self.x = 0.5 * np.random.rand(self.N)
        self.y = np.random.rand(self.N)

    # ****************************************
    # Simulation and Drawing
    # ****************************************
    def step(self):
        """
        Moves one particle to the other side.
        """
        i = np.random.randint(0, self.N)
        if self.x[i] < 0.5:
            self.nleft -= 1  # Move to right
            self.x[i] = 0.5 * (1 + np.random.rand())
        else:
            self.nleft += 1  # Move to left
            self.x[i] = 0.5 * np.random.rand()
        self.time += 1

    def draw(self, ax):
        """
        Draws particles and the partitioned box on a Matplotlib Axes object.
        """
        ax.clear()
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axvline(0.5, ymin=0.55, ymax=1.0, color='black')
        ax.axvline(0.5, ymin=0, ymax=0.45, color='black')
        ax.scatter(self.x, self.y, s=10, color='red')
        ax.set_title(f"Time: {self.time}, N_left: {self.nleft}")
