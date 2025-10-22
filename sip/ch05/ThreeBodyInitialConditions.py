import numpy as np

# ****************************************
# ThreeBodyInitialConditions Class
# ****************************************
class ThreeBodyInitialConditions:
    """
    ThreeBodyInitialConditions stores interesting initial conditions for the 
    three-body problem as NumPy arrays.
    """
    sn = np.sin(np.pi / 3)
    half = np.cos(np.pi / 3)
    x1 = 0.97000436
    v1 = 0.93240737 / 2
    y1 = 0.24308753
    v2 = 0.86473146 / 2
    v = 0.8  # initial speed

    # ****************************************
    # Initial Conditions
    # ****************************************
    # EULER: places masses on a line
    EULER = np.array([
        0, 0, 0, 0, 
        1, 0, 0, v, 
        -1, 0, 0, -v
    ])

    # LAGRANGE: places masses on an equilateral triangle
    LAGRANGE = np.array([
        1, 0, 0, v, 
        -half, -v * sn, sn, -v * half, 
        -half, v * sn, -sn, -v * half
    ])

    # MONTGOMERY: a specific stable configuration
    MONTGOMERY = np.array([
        x1, v1, -y1, v2, 
        -x1, v1, y1, v2, 
        0, -2 * v1, 0, -2 * v2
    ])
