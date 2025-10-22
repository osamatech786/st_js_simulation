import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp

# ****************************************
# Projectile Class
# ****************************************
class Projectile:
    """
    Projectile models the dynamics of a projectile and provides methods for 
    simulation and visualization.
    """
    g = 9.8

    def __init__(self, x, vx, y, vy, dt=0.01):
        """
        Initializes the projectile with a given state and time step.
        
        :param x: Initial x-position.
        :param vx: Initial x-velocity.
        :param y: Initial y-position.
        :param vy: Initial y-velocity.
        :param dt: Time step for the simulation.
        """
        # state = [x, vx, y, vy, t]
        self.state = np.array([x, vx, y, vy, 0.0])
        self.dt = dt
        self.pix_radius = 6

    def set_step_size(self, dt):
        """
        Sets the time step for the simulation.
        
        :param dt: The new time step.
        """
        self.dt = dt

    def step(self):
        """
        Advances the simulation by one time step using an ODE solver.
        """
        t_span = [self.state[4], self.state[4] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy, 
            t_span, 
            self.state[:-1], 
            t_eval=t_span
        )
        
        # Update the state with the new values
        new_state = sol.y[:, -1]
        self.state[0] = new_state[0]  # x
        self.state[1] = new_state[1]  # vx
        self.state[2] = new_state[2]  # y
        self.state[3] = new_state[3]  # vy
        self.state[4] += self.dt      # t

    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time.
        :param state: Current state [x, vx, y, vy].
        :return: The rate of change [dx/dt, dvx/dt, dy/dt, dvy/dt].
        """
        rate = np.zeros(4)
        rate[0] = state[1]  # dx/dt = vx
        rate[1] = 0         # dvx/dt = 0
        rate[2] = state[3]  # dy/dt = vy
        rate[3] = -self.g   # dvy/dt = -g
        return rate

    def draw(self, ax):
        """
        Draws the projectile and the ground on a Matplotlib Axes object.
        
        :param ax: The Matplotlib Axes to draw on.
        """
        # Draw the projectile as a circle
        circle = patches.Circle(
            (self.state[0], self.state[2]), 
            self.pix_radius / 72,  # Convert pixels to inches for display
            color='red'
        )
        ax.add_artist(circle)
        
        # Draw the ground
        ax.axhline(0, color='green')
