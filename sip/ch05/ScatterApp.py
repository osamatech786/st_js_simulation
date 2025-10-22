import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Scattering Simulation", layout="wide")
st.title("💥 Scattering Simulation")
st.write("This app simulates the scattering of particles and computes differential cross sections.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
vx = st.sidebar.number_input("Initial Velocity (vx)", value=3.0)
bmax = st.sidebar.number_input("Max Impact Parameter (bmax)", value=0.25)
db = st.sidebar.number_input("Impact Parameter Increment (db)", value=0.01, format="%.4f")

# ****************************************
# Trajectory Calculation
# ****************************************
def calculate_trajectory(b, vx):
    x = -5
    y = b
    vy = 0
    dt = 0.01
    x_history = [x]
    y_history = [y]
    
    while x < 5:
        r = np.sqrt(x**2 + y**2)
        ax = x / r**3
        ay = y / r**3
        vx = vx + ax * dt
        vy = ay * dt
        x = x + vx * dt
        y = y + vy * dt
        x_history.append(x)
        y_history.append(y)
        
    return x_history, y_history, np.arctan2(vy, vx)

# ****************************************
# Simulation Logic and Display
# ****************************************
if st.sidebar.button("Run Simulation"):
    b = db / 2
    angles = []
    impact_parameters = []

    fig1, ax1 = plt.subplots()
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.plot([0], [0], 'ro', markersize=10) # Scattering center

    while b <= bmax:
        x_traj, y_traj, angle = calculate_trajectory(b, vx)
        ax1.plot(x_traj, y_traj, '-')
        angles.append(angle)
        impact_parameters.append(b)
        b += db

    st.subheader("Trajectories")
    st.pyplot(fig1)

    st.subheader("Differential Cross Section")
    fig2, ax2 = plt.subplots()
    hist, bin_edges = np.histogram(np.abs(angles), bins=10, range=(0, np.pi))
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    cross_section = hist / (2 * np.pi * np.sin(bin_centers) * db)
    ax2.plot(bin_centers, cross_section, 'o-')
    ax2.set_xlabel("Scattering Angle (radians)")
    ax2.set_ylabel("Differential Cross Section")
    st.pyplot(fig2)
