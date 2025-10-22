import numpy as np
from scipy.integrate import solve_ivp

# ****************************************
# DampedDrivenPendulum Class
# ****************************************
class DampedDrivenPendulum:
    """
    DampedDrivenPendulum models a damped driven pendulum, adapted for use 
    with Scipy.
    """
    def __init__(self, gamma, A, initial_state):
        """
        Initializes the damped driven pendulum.
        
        :param gamma: Damping constant.
        :param A: Amplitude of the external force.
        :param initial_state: Initial state [theta, angular velocity, time].
        """
        self.gamma = gamma
        self.A = A
        self.state = np.array(initial_state)

    # ****************************************
    # Initialization and State Management
    # ****************************************
    def initialize_state(self, new_state):
        """
        Initializes the state by copying the given array into the state array.
        
        :param new_state: The new state [theta, angular velocity, time].
        """
        self.state = np.array(new_state)

    def get_state(self):
        """
        Gets the state.
        
        :return: The state array [theta, angular velocity, time].
        """
        return self.state

    # ****************************************
    # ODE Solver and Rate Calculation
    # ****************************************
    def get_rate_scipy(self, t, state):
        """
        Gets the rate using the given state for use with solve_ivp.
        
        :param t: Current time.
        :param state: Current state [theta, angular velocity].
        :return: The rate of change [dtheta/dt, domega/dt].
        """
        theta, omega = state
        dtheta_dt = omega
        domega_dt = -self.gamma * omega - (1.0 + 2.0 * self.A * np.cos(2 * t)) * np.sin(theta)
        return [dtheta_dt, domega_dt]
