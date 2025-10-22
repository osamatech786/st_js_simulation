import numpy as np
from scipy.integrate import solve_ivp

class RC:
    """
    RC models a simple RC circuit and is designed for use with an ODE solver.
    """
    def __init__(self, r, c, omega):
        """
        Constructs an RC circuit with the given resistance, capacitance, and angular frequency.
        
        :param r: Resistance.
        :param c: Capacitance.
        :param omega: Angular frequency of the source voltage.
        """
        self.r = r
        self.c = c
        self.omega = omega
        # state = [charge, time]
        self.state = np.array([0.0, 0.0])

    def get_state(self):
        """
        Returns the current state of the circuit.
        
        :return: The state array [charge, time].
        """
        return self.state

    def get_source_voltage(self, t):
        """
        Calculates the source voltage at a given time.
        
        :param t: The time.
        :return: The source voltage.
        """
        return 10 * np.sin(self.omega * t)

    def get_rate(self, t, state):
        """
        Calculates the rate of change for the ODE solver.
        
        :param t: Current time.
        :param state: Current state [charge].
        :return: The rate of change [dQ/dt].
        """
        # This method is designed for use with solve_ivp, which expects a 1D state array.
        # The time is passed as a separate argument `t`.
        charge = state[0]
        dq_dt = (-charge / (self.r * self.c)) + (self.get_source_voltage(t) / self.r)
        return [dq_dt]
