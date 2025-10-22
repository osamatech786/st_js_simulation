import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Two Planet Simulation", layout="wide")
st.title("🪐 Two Planet Simulation")
st.write("This app simulates the motion of two interacting planets orbiting a star.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
x1_0 = st.sidebar.number_input("Initial x1 (AU)", value=2.52)
vy1_0 = st.sidebar.number_input("Initial vy1", value=np.sqrt(4 * np.pi**2 / 2.52))
x2_0 = st.sidebar.number_input("Initial x2 (AU)", value=5.24)
vy2_0 = st.sidebar.number_input("Initial vy2", value=np.sqrt(4 * np.pi**2 / 5.24))
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")

G = 4 * np.pi**2

# ****************************************
# Session State Initialization
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

if 'x1_history' not in st.session_state:
    st.session_state.x1_history = [x1_0]
    st.session_state.y1_history = [0]
    st.session_state.x2_history = [x2_0]
    st.session_state.y2_history = [0]
    st.session_state.x1, st.session_state.y1, st.session_state.vx1, st.session_state.vy1 = x1_0, 0, 0, vy1_0
    st.session_state.x2, st.session_state.y2, st.session_state.vx2, st.session_state.vy2 = x2_0, 0, 0, vy2_0

# ****************************************
# UI Layout
# ****************************************
st.subheader("Orbits")
plot_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running:
    r1 = np.sqrt(st.session_state.x1**2 + st.session_state.y1**2)
    r2 = np.sqrt(st.session_state.x2**2 + st.session_state.y2**2)
    
    ax1 = -G * st.session_state.x1 / r1**3
    ay1 = -G * st.session_state.y1 / r1**3
    ax2 = -G * st.session_state.x2 / r2**3
    ay2 = -G * st.session_state.y2 / r2**3
    
    st.session_state.vx1 += ax1 * dt
    st.session_state.vy1 += ay1 * dt
    st.session_state.x1 += st.session_state.vx1 * dt
    st.session_state.y1 += st.session_state.vy1 * dt
    
    st.session_state.vx2 += ax2 * dt
    st.session_state.vy2 += ay2 * dt
    st.session_state.x2 += st.session_state.vx2 * dt
    st.session_state.y2 += st.session_state.vy2 * dt
    
    st.session_state.x1_history.append(st.session_state.x1)
    st.session_state.y1_history.append(st.session_state.y1)
    st.session_state.x2_history.append(st.session_state.x2)
    st.session_state.y2_history.append(st.session_state.y2)

    fig, ax = plt.subplots()
    ax.plot(st.session_state.x1_history, st.session_state.y1_history, 'b-')
    ax.plot(st.session_state.x2_history, st.session_state.y2_history, 'r-')
    ax.plot([0], [0], 'yo', markersize=10) # Sun
    ax.plot([st.session_state.x1], [st.session_state.y1], 'bo') # Planet 1
    ax.plot([st.session_state.x2], [st.session_state.y2], 'ro') # Planet 2
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    plot_placeholder.pyplot(fig)
    plt.close(fig)
    
    time.sleep(0.01)
