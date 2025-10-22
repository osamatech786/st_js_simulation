import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp

# ****************************************
# Planet Class
# ****************************************
class Planet:
    """
    Planet models and displays the motion of a planet using an inverse square 
    force law, adapted for use with Scipy and Matplotlib.
    """
    GM = 4 * np.pi**2  # GM in units of (AU)^3/(yr)^2

    def __init__(self, x, vx, y, vy, dt=0.01):
        """
        Initializes the planet's state and the ODE solver.
        
        :param x: Initial x-position.
        :param vx: Initial x-velocity.
        :param y: Initial y-position.
        :param vy: Initial y-velocity.
        :param dt: Time step for the simulation.
        """
        self.state = np.array([x, vx, y, vy, 0.0])  # {x, vx, y, vy, t}
        self.dt = dt
        self.trail = []

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def do_step(self):
        """
        Steps the differential equation and appends data to the trail.
        """
        t_span = [self.state[4], self.state[4] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy,
            t_span,
            self.state[:-1],  # Pass [x, vx, y, vy] to the solver
            t_eval=t_span
        )
        
        # Update state with the latest values from the solver
        new_state = sol.y[:, -1]
        self.state[0:4] = new_state
        self.state[4] += self.dt  # Increment time
        
        # Add the new position to the trail
        self.trail.append((self.state[0], self.state[2]))

    def initialize(self, init_state, dt=0.01):
        """
        Initializes the planet's position, velocity, and time.
        
        :param init_state: The initial state [x, vx, y, vy].
        :param dt: The time step.
        """
        self.state = np.append(init_state, 0.0) # Add time t=0
        self.dt = dt
        self.trail.clear()

    # ****************************************
    # ODE Solver and Rate Calculation
    # ****************************************
    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time (required by solve_ivp).
        :param state: Current state [x, vx, y, vy].
        :return: The rate of change [dx/dt, dvx/dt, dy/dt, dvy/dt].
        """
        r2 = state[0]**2 + state[2]**2  # r squared
        r3 = r2 * np.sqrt(r2)           # r cubed
        
        rate = np.zeros(4)
        rate[0] = state[1]              # dx/dt = vx
        rate[1] = -self.GM * state[0] / r3  # dvx/dt = ax
        rate[2] = state[3]              # dy/dt = vy
        rate[3] = -self.GM * state[2] / r3  # dvy/dt = ay
        return rate

    # ****************************************
    # Drawing and Visualization
    # ****************************************
    def draw(self, ax):
        """
        Draws the planet and its path on a Matplotlib Axes object.
        
        :param ax: The Matplotlib Axes to draw on.
        """
        # Draw the planet
        planet_circle = patches.Circle((self.state[0], self.state[2]), 0.05, color='blue')
        ax.add_patch(planet_circle)
        
        # Draw the trail
        if self.trail:
            trail_x, trail_y = zip(*self.trail)
            ax.plot(trail_x, trail_y, color='gray', linestyle='--')
