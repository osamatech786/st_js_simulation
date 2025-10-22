import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.integrate import solve_ivp

# ****************************************
# ThreeBody Class
# ****************************************
class ThreeBody:
    """
    ThreeBody models the gravitational three-body problem, adapted for use 
    with Scipy and Matplotlib.
    """
    def __init__(self, state, dt=0.01):
        """
        Initializes the three-body system.
        
        :param state: Initial state array {x1, vx1, y1, vy1, x2, vx2, y2, vy2, x3, vx3, y3, vy3}.
        :param dt: Time step for the simulation.
        """
        self.n = 3
        self.state = np.append(state, 0.0)  # Add time t=0
        self.dt = dt
        self.trails = [[] for _ in range(self.n)]

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def do_step(self):
        """
        Steps the differential equation and updates the trails.
        """
        t_span = [self.state[-1], self.state[-1] + self.dt]
        sol = solve_ivp(
            self.get_rate_scipy,
            t_span,
            self.state[:-1],
            t_eval=t_span
        )
        
        self.state[:-1] = sol.y[:, -1]
        self.state[-1] += self.dt
        
        for i in range(self.n):
            self.trails[i].append((self.state[4 * i], self.state[4 * i + 2]))

    def initialize(self, init_state, dt=0.01):
        """
        Initializes the positions and velocities.
        """
        self.state = np.append(init_state, 0.0)
        self.dt = dt
        for trail in self.trails:
            trail.clear()

    # ****************************************
    # Force and Rate Calculation
    # ****************************************
    def compute_force(self, state):
        """
        Computes the forces using pairwise interactions assuming equal mass.
        """
        force = np.zeros(2 * self.n)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                dx = state[4 * i] - state[4 * j]
                dy = state[4 * i + 2] - state[4 * j + 2]
                r2 = dx**2 + dy**2
                r3 = r2 * np.sqrt(r2)
                
                if r3 == 0: continue

                fx = dx / r3
                fy = dy / r3
                
                force[2 * i] -= fx
                force[2 * i + 1] -= fy
                force[2 * j] += fx
                force[2 * j + 1] += fy
        return force

    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        """
        force = self.compute_force(state)
        rate = np.zeros(4 * self.n)
        for i in range(self.n):
            i4 = 4 * i
            rate[i4] = state[i4 + 1]
            rate[i4 + 1] = force[2 * i]
            rate[i4 + 2] = state[i4 + 3]
            rate[i4 + 3] = force[2 * i + 1]
        return rate

    # ****************************************
    # Drawing and Visualization
    # ****************************************
    def draw(self, ax):
        """
        Draws the three bodies and their trails.
        """
        colors = ['blue', 'red', 'green']
        for i in range(self.n):
            # Body
            body = patches.Circle((self.state[4 * i], self.state[4 * i + 2]), 0.05, color=colors[i])
            ax.add_patch(body)
            
            # Trail
            if self.trails[i]:
                x, y = zip(*self.trails[i])
                ax.plot(x, y, color=colors[i], linestyle='--')
