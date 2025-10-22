import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp

# ****************************************
# Planet2 Class
# ****************************************
class Planet2:
    """
    Planet2 models two interacting planets in the presence of a central inverse 
    square law force, adapted for use with Scipy and Matplotlib.
    """
    GM = 4 * np.pi**2
    GM1 = 0.04 * GM
    GM2 = 0.001 * GM

    def __init__(self, x1, vx1, y1, vy1, x2, vx2, y2, vy2, dt=0.01):
        """
        Initializes the two-planet system.
        """
        self.state = np.array([x1, vx1, y1, vy1, x2, vx2, y2, vy2, 0.0])
        self.dt = dt
        self.mass1_trail = []
        self.mass2_trail = []

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def do_step(self):
        """
        Steps the differential equation and updates the trails.
        """
        t_span = [self.state[8], self.state[8] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy,
            t_span,
            self.state[:-1],
            t_eval=t_span
        )
        
        self.state[0:8] = sol.y[:, -1]
        self.state[8] += self.dt
        
        self.mass1_trail.append((self.state[0], self.state[2]))
        self.mass2_trail.append((self.state[4], self.state[6]))

    def initialize(self, init_state, dt=0.01):
        """
        Initializes the positions and velocities.
        """
        self.state = np.append(init_state, 0.0)
        self.dt = dt
        self.mass1_trail.clear()
        self.mass2_trail.clear()

    # ****************************************
    # ODE Solver and Rate Calculation
    # ****************************************
    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        """
        r1_squared = state[0]**2 + state[2]**2
        r1_cubed = r1_squared * np.sqrt(r1_squared)
        r2_squared = state[4]**2 + state[6]**2
        r2_cubed = r2_squared * np.sqrt(r2_squared)
        
        dx = state[4] - state[0]
        dy = state[6] - state[2]
        dr2 = dx**2 + dy**2
        dr3 = np.sqrt(dr2) * dr2
        
        rate = np.zeros(8)
        rate[0] = state[1]
        rate[2] = state[3]
        rate[4] = state[5]
        rate[6] = state[7]
        
        rate[1] = (-self.GM * state[0] / r1_cubed) + (self.GM1 * dx / dr3)
        rate[3] = (-self.GM * state[2] / r1_cubed) + (self.GM1 * dy / dr3)
        rate[5] = (-self.GM * state[4] / r2_cubed) - (self.GM2 * dx / dr3)
        rate[7] = (-self.GM * state[6] / r2_cubed) - (self.GM2 * dy / dr3)
        
        return rate

    # ****************************************
    # Drawing and Visualization
    # ****************************************
    def draw(self, ax):
        """
        Draws the two planets and their trails.
        """
        # Planet 1
        p1 = patches.Circle((self.state[0], self.state[2]), 0.05, color='blue')
        ax.add_patch(p1)
        if self.mass1_trail:
            x, y = zip(*self.mass1_trail)
            ax.plot(x, y, color='blue', linestyle='--')
            
        # Planet 2
        p2 = patches.Circle((self.state[4], self.state[6]), 0.03, color='red')
        ax.add_patch(p2)
        if self.mass2_trail:
            x, y = zip(*self.mass2_trail)
            ax.plot(x, y, color='red', linestyle='--')
