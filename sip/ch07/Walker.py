import numpy as np

# ****************************************
# Walker Class
# ****************************************
class Walker:
    """
    Simulates a 1D random walk and accumulates data on the walker's displacement.
    """
    def __init__(self, N, p):
        """
        Initializes the simulation parameters.
        
        :param N: Maximum number of steps.
        :param p: Probability of a step to the right.
        """
        self.N = N
        self.p = p
        self.x_accum = np.zeros(N + 1, dtype=int)
        self.x_squared_accum = np.zeros(N + 1, dtype=int)
        self.position = 0

    # ****************************************
    # Initialization
    # ****************************************
    def initialize(self):
        """
        Initializes the walker's data arrays.
        """
        self.x_accum = np.zeros(self.N + 1, dtype=int)
        self.x_squared_accum = np.zeros(self.N + 1, dtype=int)

    # ****************************************
    # Simulation Step
    # ****************************************
    def step(self):
        """
        Performs a random walk for one walker.
        """
        self.position = 0
        for t in range(self.N):
            if np.random.rand() < self.p:
                self.position += 1
            else:
                self.position -= 1
            self.x_accum[t + 1] += self.position
            self.x_squared_accum[t + 1] += self.position**2
