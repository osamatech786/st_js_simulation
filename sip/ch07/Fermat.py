import numpy as np

# ****************************************
# Fermat Class
# ****************************************
class Fermat:
    """
    Represents a light ray passing through media with varying indices of refraction.
    """
    def __init__(self, N, dn, dy=0.1):
        """
        Initializes the simulation parameters.
        
        :param N: Number of media.
        :param dn: Change in the index of refraction between media.
        :param dy: Maximum change in the y-position for each step.
        """
        self.N = N
        self.dn = dn
        self.dy = dy
        self.y = np.zeros(N + 1)
        self.v = np.zeros(N)
        self.steps = 0
        self.initialize()

    # ****************************************
    # Initialization
    # ****************************************
    def initialize(self):
        """
        Initializes the arrays for the simulation.
        """
        self.y = np.arange(self.N + 1)
        index_of_refraction = 1.0
        for i in range(self.N):
            self.v[i] = 1.0 / index_of_refraction
            index_of_refraction += self.dn
        self.steps = 0

    # ****************************************
    # Simulation Step
    # ****************************************
    def step(self):
        """
        Performs a random change in the path and accepts it if it reduces the travel time.
        """
        i = np.random.randint(1, self.N)
        y_trial = self.y[i] + 2.0 * self.dy * (np.random.rand() - 0.5)
        
        # Time in the previous configuration
        prev_time = (np.sqrt((self.y[i-1] - self.y[i])**2 + 1) / self.v[i-1] +
                     np.sqrt((self.y[i+1] - self.y[i])**2 + 1) / self.v[i])
        
        # Time in the trial configuration
        trial_time = (np.sqrt((self.y[i-1] - y_trial)**2 + 1) / self.v[i-1] +
                      np.sqrt((self.y[i+1] - y_trial)**2 + 1) / self.v[i])
        
        if trial_time < prev_time:
            self.y[i] = y_trial
            
        self.steps += 1
