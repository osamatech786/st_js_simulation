import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ****************************************
# Lorenz Class
# ****************************************
class Lorenz:
    """
    Lorenz model, adapted for use with Scipy and Matplotlib.
    """
    def __init__(self, a=28.0, b=2.667, c=10.0, dt=0.01):
        """
        Initializes the Lorenz system.
        
        :param a: Lorenz parameter 'a'.
        :param b: Lorenz parameter 'b'.
        :param c: Lorenz parameter 'c'.
        :param dt: Time step for the simulation.
        """
        self.a, self.b, self.c = a, b, c
        self.dt = dt
        self.state = np.zeros(4)
        self.trail = []

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def do_step(self):
        """
        Performs one animation step.
        """
        t_span = [self.state[3], self.state[3] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy,
            t_span,
            self.state[:-1],
            t_eval=t_span
        )
        
        self.state[0:3] = sol.y[:, -1]
        self.state[3] += self.dt
        self.trail.append(self.state[0:3].copy())

    def initialize(self, x, y, z):
        """
        Initializes the state of the Lorenz system.
        
        :param x: Initial x-coordinate.
        :param y: Initial y-coordinate.
        :param z: Initial z-coordinate.
        """
        self.state = np.array([x, y, z, 0.0])
        self.trail = [self.state[0:3].copy()]

    # ****************************************
    # ODE Solver and Rate Calculation
    # ****************************************
    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time.
        :param state: Current state [x, y, z].
        :return: The rate of change [dx/dt, dy/dt, dz/dt].
        """
        x, y, z = state
        dx_dt = -self.c * (x - y)
        dy_dt = -y - x * z + self.a * x
        dz_dt = x * y - self.b * z
        return [dx_dt, dy_dt, dz_dt]

    # ****************************************
    # Plotting
    # ****************************************
    def plot_trail(self, ax):
        """
        Plots the trail of the Lorenz attractor in 3D.
        
        :param ax: A Matplotlib 3D Axes object.
        """
        if not self.trail:
            return
            
        trail_arr = np.array(self.trail)
        ax.plot(trail_arr[:, 0], trail_arr[:, 1], trail_arr[:, 2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Lorenz Attractor")
