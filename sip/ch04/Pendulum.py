import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp

# ****************************************
# Pendulum Class
# ****************************************
class Pendulum:
    """
    Pendulum models the dynamics of a pendulum and provides methods for 
    simulation and visualization.
    """
    def __init__(self, theta, theta_dot, dt=0.01, g_over_L=3):
        """
        Initializes the pendulum with a given state and time step.
        
        :param theta: Initial angle (radians).
        :param theta_dot: Initial angular velocity (radians/s).
        :param dt: Time step for the simulation.
        :param g_over_L: Ratio of gravitational acceleration to pendulum length.
        """
        # state = [theta, theta_dot, t]
        self.state = np.array([theta, theta_dot, 0.0])
        self.dt = dt
        self.omega0_squared = g_over_L
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
        t_span = [self.state[2], self.state[2] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy, 
            t_span, 
            self.state[:-1], 
            t_eval=t_span
        )
        
        # Update the state with the new values
        new_state = sol.y[:, -1]
        self.state[0] = new_state[0]  # theta
        self.state[1] = new_state[1]  # theta_dot
        self.state[2] += self.dt      # t

    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time.
        :param state: Current state [theta, theta_dot].
        :return: The rate of change [dtheta/dt, dtheta_dot/dt].
        """
        rate = np.zeros(2)
        rate[0] = state[1]  # dtheta/dt = theta_dot
        rate[1] = -self.omega0_squared * np.sin(state[0])
        return rate

    def draw(self, ax):
        """
        Draws the pendulum on a Matplotlib Axes object.
        
        :param ax: The Matplotlib Axes to draw on.
        """
        # Pivot point
        pivot_x, pivot_y = 0, 0
        
        # Bob position
        bob_x = np.sin(self.state[0])
        bob_y = -np.cos(self.state[0])
        
        # Draw the string
        ax.plot([pivot_x, bob_x], [pivot_y, bob_y], color='black')
        
        # Draw the bob
        bob = patches.Circle((bob_x, bob_y), self.pix_radius / 72, color='red')
        ax.add_patch(bob)
