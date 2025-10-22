import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# ScatterAnalysis Class
# ****************************************
class ScatterAnalysis:
    """
    ScatterAnalysis accumulates particle scattering data and plots the 
    differential cross section using Matplotlib.
    """
    def __init__(self, num_bins=18):
        """
        Initializes the ScatterAnalysis.
        
        :param num_bins: The number of bins for the histogram.
        """
        self.num_bins = num_bins
        self.bins = np.zeros(num_bins)
        self.dtheta = np.pi / num_bins
        self.total_N = 0

    # ****************************************
    # Data Handling
    # ****************************************
    def clear(self):
        """
        Clears the cross-section data.
        """
        self.bins = np.zeros(self.num_bins)
        self.total_N = 0

    def detect_particle(self, b, theta):
        """
        Detects a particle and accumulates cross-section data.
        
        :param b: The impact parameter.
        :param theta: The scattering angle.
        """
        theta = np.abs(theta)
        index = int(theta / self.dtheta)
        if 0 <= index < self.num_bins:
            self.bins[index] += b
            self.total_N += b

    # ****************************************
    # Plotting
    # ****************************************
    def plot_cross_section(self, radius, ax):
        """
        Plots the cross-section data on a Matplotlib Axes object.
        
        :param radius: The beam radius.
        :param ax: The Matplotlib Axes to plot on.
        """
        target_density = 1 / (np.pi * radius**2)
        delta = self.dtheta * 180 / np.pi
        
        angles = (np.arange(self.num_bins) + 0.5) * delta
        domega = 2 * np.pi * np.sin((np.arange(self.num_bins) + 0.5) * self.dtheta) * self.dtheta
        
        # Avoid division by zero
        sigma = np.divide(
            self.bins, 
            self.total_N * target_density * domega, 
            out=np.zeros_like(self.bins, dtype=float), 
            where=(self.total_N * target_density * domega) != 0
        )
        
        ax.plot(angles, sigma, marker='o', linestyle='-')
        ax.set_xlabel("Angle (degrees)")
        ax.set_ylabel("Sigma")
        ax.set_title("Differential Cross Section")
        ax.grid(True)
