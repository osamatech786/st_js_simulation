import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Electric Field from Point Charges")

# ****************************************
# [Session State Initialization]
# ****************************************
if 'charges' not in st.session_state:
    st.session_state.charges = pd.DataFrame(columns=['x', 'y', 'q'])

# ****************************************
# [E-Field Calculation with Caching]
# ****************************************
@st.cache_data
def calculate_e_field(charges_df, n, a):
    """Calculates the electric field on a grid."""
    grid_points = np.linspace(-a / 2, a / 2, n)
    xx, yy = np.meshgrid(grid_points, grid_points)
    
    ex = np.zeros((n, n))
    ey = np.zeros((n, n))

    if charges_df.empty:
        return xx, yy, ex, ey

    for _, charge in charges_df.iterrows():
        dx = xx - charge['x']
        dy = yy - charge['y']
        r_squared = dx**2 + dy**2
        # Avoid division by zero at the charge location
        r_squared[r_squared == 0] = 1e-9
        r_cubed = r_squared * np.sqrt(r_squared)
        
        ex += charge['q'] * dx / r_cubed
        ey += charge['q'] * dy / r_cubed
        
    return xx, yy, ex, ey

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Controls")
n = st.sidebar.select_slider("Grid Size (n x n)", options=[10, 20, 30, 40], value=20)
a = st.sidebar.slider("Grid Length (a)", 5.0, 20.0, 10.0, 0.5)

st.sidebar.subheader("Add a New Charge")
new_x = st.sidebar.number_input("x", -a/2, a/2, 0.0, 0.1)
new_y = st.sidebar.number_input("y", -a/2, a/2, 0.0, 0.1)
new_q = st.sidebar.number_input("q (charge)", -5.0, 5.0, 1.0, 0.1)

if st.sidebar.button("Add Charge"):
    new_charge = pd.DataFrame([{'x': new_x, 'y': new_y, 'q': new_q}])
    st.session_state.charges = pd.concat([st.session_state.charges, new_charge], ignore_index=True)

if st.sidebar.button("Reset"):
    st.session_state.charges = pd.DataFrame(columns=['x', 'y', 'q'])
    st.rerun()

st.sidebar.header("Current Charges")
st.session_state.charges = st.sidebar.data_editor(st.session_state.charges, num_rows="dynamic")

# ****************************************
# [Main Display]
# ****************************************
st.subheader("Electric Field Vector Plot")

# Calculate the E-field (this will be cached)
xx, yy, ex, ey = calculate_e_field(st.session_state.charges, n, a)
magnitude = np.sqrt(ex**2 + ey**2)

fig, ax = plt.subplots(figsize=(10, 10))

# Plot the vector field
# The color of the arrows is determined by the magnitude
quiver = ax.quiver(xx, yy, ex, ey, magnitude, cmap='viridis')
fig.colorbar(quiver, ax=ax, label="Field Magnitude")

# Plot the charges
if not st.session_state.charges.empty:
    positive_charges = st.session_state.charges[st.session_state.charges['q'] > 0]
    negative_charges = st.session_state.charges[st.session_state.charges['q'] <= 0]
    ax.scatter(positive_charges['x'], positive_charges['y'], c='r', s=100, marker='o', label='Positive')
    ax.scatter(negative_charges['x'], negative_charges['y'], c='b', s=100, marker='o', label='Negative')
    ax.legend()

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Electric Field")
ax.set_xlim(-a/2, a/2)
ax.set_ylim(-a/2, a/2)
ax.set_aspect('equal', adjustable='box')
ax.grid(True)

st.pyplot(fig)
