import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Lorenz Attractor", layout="wide")
st.title("🦋 Lorenz Attractor")
st.write("This app simulates the Lorenz attractor, a classic example of a chaotic system.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
x0 = st.sidebar.number_input("Initial x", value=2.0)
y0 = st.sidebar.number_input("Initial y", value=5.0)
z0 = st.sidebar.number_input("Initial z", value=20.0)
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")
n_steps = st.sidebar.number_input("Number of Steps", value=5000, step=100)

sigma = 10
rho = 28
beta = 8/3

# ****************************************
# Session State Initialization
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running
    st.session_state.x_history = [x0]
    st.session_state.y_history = [y0]
    st.session_state.z_history = [z0]
    st.session_state.x, st.session_state.y, st.session_state.z = x0, y0, z0

if 'x_history' not in st.session_state:
    st.session_state.x_history = [x0]
    st.session_state.y_history = [y0]
    st.session_state.z_history = [z0]
    st.session_state.x, st.session_state.y, st.session_state.z = x0, y0, z0

# ****************************************
# UI Layout and Plotting
# ****************************************
st.subheader("Trajectory")
plot_placeholder = st.empty()

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-20, 20)
ax.set_ylim(-30, 30)
ax.set_zlim(0, 50)
line, = ax.plot([], [], [], lw=0.5)

def update_plot():
    line.set_data(st.session_state.x_history, st.session_state.y_history)
    line.set_3d_properties(st.session_state.z_history)
    plot_placeholder.pyplot(fig)

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running and len(st.session_state.x_history) < n_steps:
    dx = sigma * (st.session_state.y - st.session_state.x)
    dy = st.session_state.x * (rho - st.session_state.z) - st.session_state.y
    dz = st.session_state.x * st.session_state.y - beta * st.session_state.z
    
    st.session_state.x += dx * dt
    st.session_state.y += dy * dt
    st.session_state.z += dz * dt
    
    st.session_state.x_history.append(st.session_state.x)
    st.session_state.y_history.append(st.session_state.y)
    st.session_state.z_history.append(st.session_state.z)
    
    update_plot()
    time.sleep(0.01)
