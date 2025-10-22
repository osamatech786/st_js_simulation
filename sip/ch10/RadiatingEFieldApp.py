import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("Electric Field of a Radiating Charge")

# ****************************************
# [RadiatingCharge Class]
# ****************************************
class RadiatingCharge:
    def __init__(self, dt=0.5, vmax=0.9):
        self.dt = dt
        self.vmax = vmax
        self.c = 1.0  # Speed of light
        self.q = 1.0  # Charge
        self.reset_path()

    def reset_path(self):
        self.time = 0
        # History of position, velocity, acceleration
        self.path_x = [0.0]
        self.path_y = [0.0]
        self.vx_hist = [self.vmax]
        self.vy_hist = [0.0]
        self.ax_hist = [0.0]
        self.ay_hist = [0.0]

    def step(self):
        """Updates the charge's motion - simple harmonic motion in x."""
        self.time += self.dt
        omega = 0.1 # Oscillation frequency
        
        x = (self.vmax / omega) * np.sin(omega * self.time)
        y = 0.0
        vx = self.vmax * np.cos(omega * self.time)
        vy = 0.0
        ax = -self.vmax * omega * np.sin(omega * self.time)
        ay = 0.0
        
        self.path_x.append(x)
        self.path_y.append(y)
        self.vx_hist.append(vx)
        self.vy_hist.append(vy)
        self.ax_hist.append(ax)
        self.ay_hist.append(ay)

    def get_retarded_state(self, x, y):
        """Finds the state of the charge at the retarded time for a given point (x, y)."""
        # This is a simplified approach: we search the history for the retarded time.
        # A more robust method would use a numerical solver.
        for i in range(len(self.path_x) - 1, -1, -1):
            t_r = self.time - i * self.dt
            dist = np.sqrt((x - self.path_x[i])**2 + (y - self.path_y[i])**2)
            if np.isclose(dist, self.c * (self.time - t_r), atol=self.c * self.dt):
                return {
                    'x': self.path_x[i], 'y': self.path_y[i],
                    'vx': self.vx_hist[i], 'vy': self.vy_hist[i],
                    'ax': self.ax_hist[i], 'ay': self.ay_hist[i]
                }
        return None # No retarded time found in history

    def calculate_retarded_field(self, x, y, fields):
        """Calculates the E-field at (x, y) using Lienard-Wiechert potentials."""
        retarded_state = self.get_retarded_state(x, y)
        if retarded_state is None:
            fields[0], fields[1] = 0, 0
            return

        R_vec = np.array([x - retarded_state['x'], y - retarded_state['y']])
        R = np.linalg.norm(R_vec)
        if R == 0:
            fields[0], fields[1] = 0, 0
            return
            
        n_vec = R_vec / R
        v_vec = np.array([retarded_state['vx'], retarded_state['vy']])
        a_vec = np.array([retarded_state['ax'], retarded_state['ay']])
        
        u_vec = self.c * n_vec - v_vec
        dot_u_R = np.dot(u_vec, n_vec)
        
        term1_factor = self.q / (4 * np.pi * R**2)
        term1 = (self.c**2 - np.dot(v_vec, v_vec)) * u_vec / dot_u_R**3
        
        term2_factor = self.q / (4 * np.pi * self.c * R)
        term2 = np.cross(n_vec, np.cross(u_vec, a_vec)) / dot_u_R**3
        
        E_vec = term1_factor * term1 + term2_factor * np.array([term2[0], term2[1]]) # Simplified for 2D
        fields[0], fields[1] = E_vec[0], E_vec[1]

# ****************************************
# [UI Controls & State]
# ****************************************
st.sidebar.header("Simulation Parameters")
grid_size = st.sidebar.select_slider("Grid Size", options=[21, 31, 41], value=31)
dt = st.sidebar.slider("Time Step (dt)", 0.1, 1.0, 0.5, 0.1)
vmax = st.sidebar.slider("Max Velocity (vmax/c)", 0.1, 0.95, 0.9, 0.05)

if 'charge' not in st.session_state or st.sidebar.button("Initialize/Reset"):
    st.session_state.charge = RadiatingCharge(dt=dt, vmax=vmax)
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

# ****************************************
# [Main Display and Animation Loop]
# ****************************************
st.subheader("Radiating Electric Field")
plot_placeholder = st.empty()
info_placeholder = st.empty()

xmin, xmax, ymin, ymax = -20, 20, -20, 20
grid_x = np.linspace(xmin, xmax, grid_size)
grid_y = np.linspace(ymin, ymax, grid_size)
xx, yy = np.meshgrid(grid_x, grid_y)

def calculate_fields_on_grid(charge):
    Exy = np.zeros((2, grid_size, grid_size))
    fields = np.zeros(2)
    for i in range(grid_size):
        for j in range(grid_size):
            charge.calculate_retarded_field(grid_x[i], grid_y[j], fields)
            Exy[0, i, j], Exy[1, i, j] = fields[0], fields[1]
    return Exy

def draw_frame():
    charge = st.session_state.charge
    Exy = calculate_fields_on_grid(charge)
    magnitude = np.sqrt(Exy[0]**2 + Exy[1]**2)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.quiver(xx, yy, Exy[0], Exy[1], magnitude, cmap='viridis', scale=5.0)
    
    # Plot charge and path
    ax.plot(charge.path_x, charge.path_y, 'r-', lw=1)
    ax.plot(charge.path_x[-1], charge.path_y[-1], 'ro', markersize=10)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.set_title("Electric Field")
    plot_placeholder.pyplot(fig)
    info_placeholder.text(f"Time: {charge.time:.2f}")
    plt.close(fig)

if st.session_state.running:
    while True:
        st.session_state.charge.step()
        draw_frame()
        time.sleep(0.05)
else:
    draw_frame()
