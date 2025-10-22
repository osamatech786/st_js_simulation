import numpy as np

# ****************************************
# Nuclei Class
# ****************************************
class Nuclei:
    """
    Simulates the decay of unstable nuclei.
    """
    def __init__(self, tmax, n0, p):
        """
        Initializes the simulation parameters.
        
        :param tmax: Maximum time to record data.
        :param n0: Initial number of unstable nuclei.
        :param p: Decay probability.
        """
        self.tmax = tmax
        self.n0 = n0
        self.p = p
        self.n = np.zeros(tmax + 1, dtype=int)

    # ****************************************
    # Initialization
    # ****************************************
    def initialize(self):
        """
        Initializes the array for the number of unstable nuclei.
        """
        self.n = np.zeros(self.tmax + 1, dtype=int)

    # ****************************************
    # Simulation Step
    # ****************************************
    def step(self):
        """
        Simulates the decay of nuclei over time.
        """
        self.n[0] += self.n0
        n_unstable = self.n0
        for t in range(self.tmax):
            decays = np.sum(np.random.rand(n_unstable) < self.p)
            n_unstable -= decays
            self.n[t + 1] += n_unstable
