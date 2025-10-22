import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Electric Field Line Tracer")

# ****************************************
# [Session State Initialization]
# ****************************************
if 'charges' not in st.session_state:
    st.session_state.charges = pd.DataFrame(columns=['x', 'y', 'q'])
if 'field_lines' not in st.session_state:
    st.session_state.field_lines = pd.DataFrame(columns=['x_start', 'y_start'])

# ****************************************
# [E-Field and Field Line Calculation]
# ****************************************
def get_e_field_at_point(x, y, charges_df):
    """Calculates the electric field vector at a single point."""
    ex, ey = 0.0, 0.0
    if charges_df.empty:
        return ex, ey
    for _, charge in charges_df.iterrows():
        dx = x - charge['x']
        dy = y - charge['y']
        r_squared = dx**2 + dy**2
        if r_squared < 1e-6: # Avoid singularity
            return np.inf, np.inf
        r_cubed = r_squared * np.sqrt(r_squared)
        ex += charge['q'] * dx / r_cubed
        ey += charge['q'] * dy / r_cubed
    return ex, ey

def trace_field_line(x_start, y_start, charges_df, step_size, num_steps, bounds):
    """Traces a single electric field line."""
    path = [(x_start, y_start)]
    x, y = x_start, y_start
    
    for _ in range(num_steps):
        ex, ey = get_e_field_at_point(x, y, charges_df)
        if np.isinf(ex) or np.isinf(ey):
            break # Stop if we hit a charge
            
        magnitude = np.sqrt(ex**2 + ey**2)
        if magnitude == 0:
            break # Stop if field is zero
            
        # Move a small step in the direction of the field
        x += step_size * ex / magnitude
        y += step_size * ey / magnitude
        
        # Check if out of bounds
        if not (bounds['xmin'] < x < bounds['xmax'] and bounds['ymin'] < y < bounds['ymax']):
            break
            
        path.append((x, y))
        
    return np.array(path)

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Controls")
a = 10.0 # Viewing area side length
step_size = st.sidebar.slider("Step Size", 0.01, 0.5, 0.1, 0.01)
num_steps = st.sidebar.slider("Number of Steps", 50, 500, 200, 10)

st.sidebar.subheader("Add a New Charge")
new_charge_x = st.sidebar.number_input("Charge x", -a/2, a/2, 0.0, 0.1, key="cx")
new_charge_y = st.sidebar.number_input("Charge y", -a/2, a/2, 0.0, 0.1, key="cy")
new_q = st.sidebar.number_input("Charge q", -5.0, 5.0, 1.0, 0.1, key="cq")
if st.sidebar.button("Add Charge"):
    new_charge = pd.DataFrame([{'x': new_charge_x, 'y': new_charge_y, 'q': new_q}])
    st.session_state.charges = pd.concat([st.session_state.charges, new_charge], ignore_index=True)

st.sidebar.subheader("Add a Field Line")
line_x = st.sidebar.number_input("Start x", -a/2, a/2, 1.0, 0.1, key="lx")
line_y = st.sidebar.number_input("Start y", -a/2, a/2, 1.0, 0.1, key="ly")
if st.sidebar.button("Add Field Line"):
    new_line = pd.DataFrame([{'x_start': line_x, 'y_start': line_y}])
    st.session_state.field_lines = pd.concat([st.session_state.field_lines, new_line], ignore_index=True)

if st.sidebar.button("Reset"):
    st.session_state.charges = pd.DataFrame(columns=['x', 'y', 'q'])
    st.session_state.field_lines = pd.DataFrame(columns=['x_start', 'y_start'])
    st.rerun()

st.sidebar.header("Current Charges")
st.session_state.charges = st.sidebar.data_editor(st.session_state.charges, num_rows="dynamic", key="charges_editor")

st.sidebar.header("Field Line Starting Points")
st.session_state.field_lines = st.sidebar.data_editor(st.session_state.field_lines, num_rows="dynamic", key="lines_editor")

# ****************************************
# [Main Display]
# ****************************************
st.subheader("Electric Field Lines")
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the charges
if not st.session_state.charges.empty:
    positive = st.session_state.charges[st.session_state.charges['q'] > 0]
    negative = st.session_state.charges[st.session_state.charges['q'] <= 0]
    ax.scatter(positive['x'], positive['y'], c='r', s=100, marker='o', label='Positive')
    ax.scatter(negative['x'], negative['y'], c='b', s=100, marker='o', label='Negative')

# Trace and plot the field lines
bounds = {'xmin': -a/2, 'xmax': a/2, 'ymin': -a/2, 'ymax': a/2}
if not st.session_state.field_lines.empty:
    for _, line_start in st.session_state.field_lines.iterrows():
        # Trace line forwards
        path_fwd = trace_field_line(line_start['x_start'], line_start['y_start'], st.session_state.charges, step_size, num_steps, bounds)
        ax.plot(path_fwd[:, 0], path_fwd[:, 1], 'k-')
        # Trace line backwards
        path_bwd = trace_field_line(line_start['x_start'], line_start['y_start'], st.session_state.charges, -step_size, num_steps, bounds)
        ax.plot(path_bwd[:, 0], path_bwd[:, 1], 'k-')

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Electric Field Lines")
ax.set_xlim(-a/2, a/2)
ax.set_ylim(-a/2, a/2)
ax.set_aspect('equal', adjustable='box')
ax.grid(True)
if not st.session_state.charges.empty:
    ax.legend()

st.pyplot(fig)
