import numpy as np

# ****************************************
# FallingParticleODE Class
# ****************************************
class FallingParticleODE:
    """
    FallingParticleODE models a falling particle.
    This class is designed to be compatible with ODE solvers.
    """
    g = 9.8

    def __init__(self, y, v):
        """
        Constructs the FallingParticleODE model with the given initial position and velocity.
        
        :param y: initial position
        :param v: initial velocity
        """
        # state[0] = y (position)
        # state[1] = v (velocity)
        # state[2] = t (time)
        self.state = np.array([y, v, 0.0])

    def get_state(self):
        """
        Gets the state array.
        
        :return: the state array [y, v, t]
        """
        return self.state

    def get_rate(self, state):
        """
        Gets the rate array. The rate is computed using the given state.
        
        :param state: the current state array [y, v, t]
        :return: the rate of change array [dy/dt, dv/dt, dt/dt]
        """
        rate = np.zeros(3)
        rate[0] = state[1]  # rate of change of y is v
        rate[1] = -self.g   # rate of change of v is -g
        rate[2] = 1.0       # rate of change of time is 1
        return rate
