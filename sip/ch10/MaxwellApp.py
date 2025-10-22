import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="centered")
st.title("3D Maxwell's Equations Solver (FDTD)")

# ****************************************
# [Maxwell FDTD Simulation Class]
# ****************************************
class Maxwell:
    def __init__(self, size):
        self.size = size
        self.t = 0
        
        # E and B fields (Ex, Ey, Ez, Bx, By, Bz)
        self.E = np.zeros((3, size, size, size))
        self.B = np.zeros((3, size, size, size))
        
        # FDTD parameters (assuming c=1, dx=1, dy=1, dz=1)
        self.dt = 0.5 # Should satisfy CFL condition dt <= 1/sqrt(3) for 3D
        
        # Source parameters
        self.source_pos = (size // 2, size // 2, size // 2)
        self.source_t0 = 20.0
        self.source_width = 5.0

    def update_b_field(self):
        curl_E_x = (self.E[2, :, 1:, :] - self.E[2, :, :-1, :]) - (self.E[1, :, :, 1:] - self.E[1, :, :, :-1])
        curl_E_y = (self.E[0, :, :, 1:] - self.E[0, :, :, :-1]) - (self.E[2, 1:, :, :] - self.E[2, :-1, :, :])
        curl_E_z = (self.E[1, 1:, :, :] - self.E[1, :-1, :, :]) - (self.E[0, :, 1:, :] - self.E[0, :, :-1, :])
        
        self.B[0, :, :-1, :-1] -= self.dt * curl_E_x
        self.B[1, :-1, :, :-1] -= self.dt * curl_E_y
        self.B[2, :-1, :-1, :] -= self.dt * curl_E_z

    def update_e_field(self):
        curl_B_x = (self.B[2, :, 1:, :] - self.B[2, :, :-1, :]) - (self.B[1, :, :, 1:] - self.B[1, :, :, :-1])
        curl_B_y = (self.B[0, :, :, 1:] - self.B[0, :, :, :-1]) - (self.B[2, 1:, :, :] - self.B[2, :-1, :, :])
        curl_B_z = (self.B[1, 1:, :, :] - self.B[1, :-1, :, :]) - (self.B[0, :, 1:, :] - self.B[0, :, :-1, :])

        self.E[0, :, 1:, 1:] += self.dt * curl_B_x
        self.E[1, 1:, :, 1:] += self.dt * curl_B_y
        self.E[2, 1:, 1:, :] += self.dt * curl_B_z

    def add_source(self):
        # Add a Gaussian pulse source to Ez at the center
        pulse = np.exp(-((self.t - self.source_t0) / self.source_width)**2)
        i, j, k = self.source_pos
        self.E[2, i, j, k] += pulse

    def apply_boundary_conditions(self):
        # Simple PEC boundary conditions (tangential E = 0)
        self.E[:, 0, :, :] = 0
        self.E[:, -1, :, :] = 0
        self.E[:, :, 0, :] = 0
        self.E[:, :, -1, :] = 0
        self.E[:, :, :, 0] = 0
        self.E[:, :, :, -1] = 0

    def do_step(self):
        self.update_b_field()
        self.update_e_field()
        self.add_source()
        self.apply_boundary_conditions()
        self.t += self.dt

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Simulation Parameters")
size = st.sidebar.select_slider("Grid Size", options=[15, 31, 63], value=31)
dt_param = st.sidebar.slider("Time Step (dt)", 0.1, 0.5, 0.5, 0.1)

if 'maxwell' not in st.session_state or st.sidebar.button("Initialize/Reset"):
    st.session_state.maxwell = Maxwell(size)
    st.session_state.maxwell.dt = dt_param
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

# ****************************************
# [Main Display and Animation Loop]
# ****************************************
st.subheader("E-Field in XY Plane (Ez component)")
plot_placeholder = st.empty()
info_placeholder = st.empty()

def draw_frame():
    """Draws a single frame of the animation."""
    maxwell = st.session_state.maxwell
    mid_z = maxwell.size // 2
    # Display the Ez component in the middle xy-plane
    field_slice = maxwell.E[2, :, :, mid_z]
    
    fig, ax = plt.subplots()
    im = ax.imshow(field_slice.T, cmap='viridis', origin='lower', vmin=-0.5, vmax=0.5)
    fig.colorbar(im, ax=ax)
    ax.set_title("Ez component")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    
    plot_placeholder.pyplot(fig)
    info_placeholder.text(f"Time: {maxwell.t:.2f}")
    plt.close(fig)

# Animation loop
if st.session_state.running:
    while True:
        st.session_state.maxwell.do_step()
        draw_frame()
        time.sleep(0.01)
else:
    draw_frame()
