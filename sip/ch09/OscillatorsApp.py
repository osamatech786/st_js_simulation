import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="centered")
st.title("Coupled Oscillators Simulation")

# ****************************************
# [Oscillators Class]
# ****************************************
class Oscillators:
    def __init__(self, mode, N):
        self.N = N
        self.mode = mode
        self.time = 0.0
        self.positions = np.arange(1, N + 1)
        
        # Calculate angular frequency for the given mode
        self.omega = 2 * np.sin(self.mode * np.pi / (2 * (self.N + 1)))

    def step(self, dt):
        self.time += dt

    def get_displacements(self):
        """Calculates the displacement of each oscillator at the current time."""
        # y_j(t) = sin(j * m * pi / (N + 1)) * cos(omega_m * t)
        spatial_part = np.sin(self.positions * self.mode * np.pi / (self.N + 1))
        temporal_part = np.cos(self.omega * self.time)
        return spatial_part * temporal_part

# ****************************************
# [Session State Initialization]
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False
if 'oscillators' not in st.session_state:
    st.session_state.oscillators = Oscillators(mode=1, N=16)

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Simulation Parameters")
N = st.sidebar.number_input("Number of particles (N)", 4, 100, 16, 1)
mode = st.sidebar.number_input("Mode", 1, N, 1, 1)
dt = st.sidebar.slider("Time step (dt)", 0.01, 1.0, 0.5, 0.01)

if st.sidebar.button("Initialize/Reset"):
    st.session_state.oscillators = Oscillators(mode=mode, N=N)
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

# ****************************************
# [Main Display and Animation Loop]
# ****************************************
st.subheader("Oscillator Displacements")
plot_placeholder = st.empty()
time_placeholder = st.empty()

def draw_frame():
    """Draws a single frame of the animation."""
    osc = st.session_state.oscillators
    displacements = osc.get_displacements()
    
    fig, ax = plt.subplots()
    # Use a stem plot to show displacement from equilibrium
    markerline, stemlines, baseline = ax.stem(
        osc.positions, displacements, basefmt='k-'
    )
    plt.setp(stemlines, 'linewidth', 2)
    plt.setp(markerline, 'markersize', 8)
    
    ax.set_xlabel("Position")
    ax.set_ylabel("Displacement")
    ax.set_title("Coupled Oscillators")
    ax.set_xlim(0, osc.N + 1)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True)
    
    plot_placeholder.pyplot(fig)
    time_placeholder.write(f"Time: {osc.time:.2f}")
    plt.close(fig)

# Animation loop
if st.session_state.running:
    while True:
        st.session_state.oscillators.step(dt)
        draw_frame()
        time.sleep(0.05) # Control frame rate
else:
    # Draw a static frame if not running
    draw_frame()
