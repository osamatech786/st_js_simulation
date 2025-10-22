import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("Huygens' Principle Simulation")

# ****************************************
# [Session State Initialization]
# ****************************************
if 'sources' not in st.session_state:
    st.session_state.sources = pd.DataFrame(columns=['x', 'y'])
if 'running' not in st.session_state:
    st.session_state.running = False
if 'time' not in st.session_state:
    st.session_state.time = 0.0

# ****************************************
# [Calculation Logic with Caching]
# ****************************************
@st.cache_data
def calculate_phasors(sources_df, n, a):
    """Calculates the base real and imaginary phasors for a set of sources."""
    if sources_df.empty:
        return np.zeros((n, n)), np.zeros((n, n))

    grid_points = np.linspace(-a / 2, a / 2, n)
    xx, yy = np.meshgrid(grid_points, grid_points)
    
    total_real_phasor = np.zeros((n, n))
    total_imag_phasor = np.zeros((n, n))

    for _, source in sources_df.iterrows():
        dx = xx - source['x']
        dy = yy - source['y']
        r = np.sqrt(dx**2 + dy**2)
        
        # Avoid division by zero at the source location
        r[r == 0] = 1e-9
        
        phase = 2 * np.pi * r
        total_real_phasor += np.cos(phase) / r
        total_imag_phasor += np.sin(phase) / r
        
    return total_real_phasor, total_imag_phasor

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Controls")
n = st.sidebar.select_slider("Grid Size (n x n)", options=[64, 128, 256], value=128)
a = st.sidebar.slider("Grid Length (a)", 5.0, 20.0, 10.0, 0.5)

if st.sidebar.button("Add Source"):
    new_source = pd.DataFrame([{'x': 0.0, 'y': 0.0}])
    st.session_state.sources = pd.concat([st.session_state.sources, new_source], ignore_index=True)

if st.sidebar.button("Start/Stop Animation"):
    st.session_state.running = not st.session_state.running

if st.sidebar.button("Reset"):
    st.session_state.sources = pd.DataFrame(columns=['x', 'y'])
    st.session_state.running = False
    st.session_state.time = 0.0
    st.rerun()

st.sidebar.header("Source Positions")
st.session_state.sources = st.sidebar.data_editor(st.session_state.sources, num_rows="dynamic")

# ****************************************
# [Main Display and Animation Loop]
# ****************************************
st.subheader("Wave Intensity")
plot_placeholder = st.empty()
time_placeholder = st.empty()

# Get the base phasors (this will be cached)
real_phasor, imag_phasor = calculate_phasors(st.session_state.sources, n, a)

def draw_frame(t):
    """Draws a single frame of the animation for a given time t."""
    cos_t = np.cos(2 * np.pi * t)
    sin_t = np.sin(2 * np.pi * t)
    
    # Rotate the phasor: Re(phasor * e^(-i*omega*t))
    re_field = cos_t * real_phasor + sin_t * imag_phasor
    amplitude = re_field**2
    
    fig, ax = plt.subplots()
    im = ax.imshow(amplitude, extent=(-a/2, a/2, -a/2, a/2), cmap='hot', origin='lower')
    
    # Plot sources on top
    if not st.session_state.sources.empty:
        ax.plot(st.session_state.sources['x'], st.session_state.sources['y'], 'bo', markersize=5)
        # Set a reasonable color scale based on number of sources
        im.set_clim(0, 0.2 * len(st.session_state.sources))

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Interference Pattern")
    
    plot_placeholder.pyplot(fig)
    time_placeholder.write(f"Time: {t:.2f}")
    plt.close(fig)

# Animation loop
if st.session_state.running:
    while True:
        st.session_state.time += 0.05
        draw_frame(st.session_state.time)
        time.sleep(0.01) # Control frame rate
else:
    # Draw a static frame if not running
    draw_frame(st.session_state.time)
