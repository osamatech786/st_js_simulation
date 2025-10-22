import numpy as np

class Analyze:
    """
    Analyzes Fourier sine and cosine coefficients of a given function.
    """
    def __init__(self, f, N, delta):
        """
        Constructs the Analyze object.
        
        :param f: The function to be analyzed.
        :param N: The number of points.
        :param delta: The sampling interval.
        """
        self.f = f
        self.delta = delta
        self.N = N
        self.period = N * delta
        self.omega0 = 2 * np.pi / self.period

    def get_sine_coefficient(self, n):
        """
        Gets a Fourier sine coefficient.
        
        :param n: The coefficient index.
        :return: The coefficient.
        """
        t = np.arange(0, self.period, self.delta)
        sum_val = np.sum(self.f(t) * np.sin(n * self.omega0 * t))
        return 2 * self.delta * sum_val / self.period

    def get_cosine_coefficient(self, n):
        """
        Gets a Fourier cosine coefficient.
        
        :param n: The coefficient index.
        :return: The coefficient.
        """
        t = np.arange(0, self.period, self.delta)
        sum_val = np.sum(self.f(t) * np.cos(n * self.omega0 * t))
        return 2 * self.delta * sum_val / self.period
