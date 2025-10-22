import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Planet Simulation", layout="wide")
st.title("🪐 Planet Simulation")
st.write("This app simulates the motion of an orbiting planet.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
x0 = st.sidebar.number_input("Initial x (AU)", value=1.0)
vx0 = st.sidebar.number_input("Initial vx", value=0.0)
y0 = st.sidebar.number_input("Initial y (AU)", value=0.0)
vy0 = st.sidebar.number_input("Initial vy", value=6.28)
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")

G = 4 * np.pi**2

# ****************************************
# Session State Initialization
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

if 'x_history' not in st.session_state:
    st.session_state.x_history = [x0]
    st.session_state.y_history = [y0]
    st.session_state.x = x0
    st.session_state.y = y0
    st.session_state.vx = vx0
    st.session_state.vy = vy0

# ****************************************
# UI Layout
# ****************************************
st.subheader("Orbit")
plot_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running:
    r = np.sqrt(st.session_state.x**2 + st.session_state.y**2)
    ax = -G * st.session_state.x / r**3
    ay = -G * st.session_state.y / r**3
    
    st.session_state.vx = st.session_state.vx + ax * dt
    st.session_state.vy = st.session_state.vy + ay * dt
    st.session_state.x = st.session_state.x + st.session_state.vx * dt
    st.session_state.y = st.session_state.y + st.session_state.vy * dt
    
    st.session_state.x_history.append(st.session_state.x)
    st.session_state.y_history.append(st.session_state.y)

    fig, ax = plt.subplots()
    ax.plot(st.session_state.x_history, st.session_state.y_history, 'b-')
    ax.plot([0], [0], 'yo', markersize=10) # Sun
    ax.plot([st.session_state.x], [st.session_state.y], 'bo') # Planet
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("x (AU)")
    ax.set_ylabel("y (AU)")
    plot_placeholder.pyplot(fig)
    plt.close(fig)
    
    time.sleep(0.01)
