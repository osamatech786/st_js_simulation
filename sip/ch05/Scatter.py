import numpy as np
from scipy.integrate import solve_ivp

# ****************************************
# Scatter Class
# ****************************************
class Scatter:
    """
    Scatter models particle scattering using a central force law, adapted for 
    use with Scipy and Matplotlib.
    """
    def __init__(self, dt=0.05):
        """
        Initializes the Scatter simulation.
        
        :param dt: Time step for the simulation.
        """
        self.dt = dt
        self.state = np.zeros(5)

    # ****************************************
    # Trajectory Calculation
    # ****************************************
    def calculate_trajectory(self, b, vx):
        """
        Calculates a trajectory and returns the path.
        
        :param b: The impact parameter.
        :param vx: The initial velocity.
        :return: A list of (x, y) points representing the trajectory.
        """
        self.state = np.array([-5.0, vx, b, 0, 0])  # x, vx, y, vy, t
        trail = []
        
        r2_initial = self.state[0]**2 + self.state[2]**2
        count = 0
        
        while count <= 1000:
            trail.append((self.state[0], self.state[2]))
            
            t_span = [self.state[4], self.state[4] + self.dt]
            sol = solve_ivp(
                self.get_rate_scipy,
                t_span,
                self.state[:-1],
                t_eval=t_span
            )
            
            self.state[0:4] = sol.y[:, -1]
            self.state[4] += self.dt
            
            r2_current = self.state[0]**2 + self.state[2]**2
            if 2 * r2_initial < r2_current and count > 1:
                break
                
            count += 1
            
        return trail

    # ****************************************
    # Force and Rate Calculation
    # ****************************************
    def force(self, r):
        """
        Gets the magnitude of the central force.
        
        :param r: The distance from the center.
        :return: The force.
        """
        return 1 / r**2 if r != 0 else 0

    def get_rate_scipy(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time.
        :param state: Current state [x, vx, y, vy].
        :return: The rate of change.
        """
        r = np.sqrt(state[0]**2 + state[2]**2)
        f = self.force(r)
        
        rate = np.zeros(4)
        rate[0] = state[1]
        rate[1] = f * state[0] / r if r != 0 else 0
        rate[2] = state[3]
        rate[3] = f * state[2] / r if r != 0 else 0
        
        return rate

    # ****************************************
    # Angle Calculation
    # ****************************************
    def get_angle(self):
        """
        Gets the scattering angle.
        
        :return: The angle in radians.
        """
        return np.arctan2(self.state[3], self.state[1])
