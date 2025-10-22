import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")
st.title("Solving Laplace's Equation with Relaxation Method")

# ****************************************
# [Session State Initialization]
# ****************************************
def initialize_state(grid_size, geometry):
    """Initializes the potential and conductor arrays based on geometry."""
    potential = np.zeros((grid_size, grid_size))
    is_conductor = np.zeros((grid_size, grid_size), dtype=bool)

    # Outer boundary conductors
    is_conductor[0, :] = True
    is_conductor[-1, :] = True
    is_conductor[:, 0] = True
    is_conductor[:, -1] = True

    if geometry == "Parallel Plates":
        plate1_pos = grid_size // 3
        plate2_pos = 2 * grid_size // 3
        is_conductor[plate1_pos, 5:-5] = True
        potential[plate1_pos, 5:-5] = 100
        is_conductor[plate2_pos, 5:-5] = True
        potential[plate2_pos, 5:-5] = -100
    
    st.session_state.potential = potential
    st.session_state.is_conductor = is_conductor
    st.session_state.iteration = 0
    st.session_state.error = np.inf

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Controls")
grid_size = st.sidebar.select_slider("Grid Size", options=[31, 63, 127], value=31)
max_error = st.sidebar.number_input("Maximum Error Tolerance", 0.01, 10.0, 0.1, 0.01)
geometry = st.sidebar.selectbox("Conductor Geometry", ["Parallel Plates"])

if 'potential' not in st.session_state or st.sidebar.button("Initialize/Reset"):
    initialize_state(grid_size, geometry)
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

# ****************************************
# [Relaxation Step]
# ****************************************
def relaxation_step(potential, is_conductor):
    """Performs a single Jacobi relaxation step."""
    potential_old = potential.copy()
    
    # Average the neighbors using array slicing
    potential[1:-1, 1:-1] = (potential_old[:-2, 1:-1] + potential_old[2:, 1:-1] +
                             potential_old[1:-1, :-2] + potential_old[1:-1, 2:]) / 4.0
    
    # Ensure conductor potentials are not changed
    potential[is_conductor] = potential_old[is_conductor]
    
    # Calculate the maximum error for this step
    error = np.max(np.abs(potential - potential_old))
    return potential, error

# ****************************************
# [Main Display and Animation Loop]
# ****************************************
col1, col2 = st.columns(2)
with col1:
    st.subheader("Electric Potential (V)")
    plot_placeholder_v = st.empty()
with col2:
    st.subheader("Electric Field (E = -∇V)")
    plot_placeholder_e = st.empty()

info_placeholder = st.empty()

def draw_plots():
    """Draws the potential and E-field plots."""
    potential = st.session_state.potential
    
    # Plot Potential
    fig1, ax1 = plt.subplots()
    im = ax1.imshow(potential.T, cmap='viridis', origin='lower')
    fig1.colorbar(im, ax=ax1, label="Potential (V)")
    ax1.set_title("Potential Landscape")
    ax1.set_xticks([])
    ax1.set_yticks([])
    plot_placeholder_v.pyplot(fig1)
    plt.close(fig1)

    # Calculate and Plot E-Field
    ey, ex = np.gradient(-potential)
    fig2, ax2 = plt.subplots()
    skip = 2 # Plot fewer vectors for clarity
    ax2.quiver(np.arange(0, grid_size, skip), np.arange(0, grid_size, skip),
               ex[::skip, ::skip], ey[::skip, ::skip],
               color='r', pivot='middle')
    ax2.set_title("Electric Field")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_aspect('equal')
    plot_placeholder_e.pyplot(fig2)
    plt.close(fig2)

# Animation loop
if st.session_state.running:
    while st.session_state.error > max_error:
        st.session_state.potential, st.session_state.error = relaxation_step(
            st.session_state.potential, st.session_state.is_conductor
        )
        st.session_state.iteration += 1
        
        # Update plots and info periodically
        if st.session_state.iteration % 5 == 0:
            draw_plots()
            info_placeholder.text(f"Iteration: {st.session_state.iteration}, Max Error: {st.session_state.error:.4f}")
            time.sleep(0.01)
    
    st.session_state.running = False
    st.success(f"Converged after {st.session_state.iteration} iterations!")

# Draw final state or initial state
draw_plots()
info_placeholder.text(f"Iteration: {st.session_state.iteration}, Max Error: {st.session_state.error:.4f}")
