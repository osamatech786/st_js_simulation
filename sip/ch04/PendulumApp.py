import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Pendulum Simulation", layout="wide")
st.title("Pendulum Simulation")
st.write("This app simulates the motion of a simple pendulum.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
theta0 = st.sidebar.number_input("Initial theta (radians)", value=0.2)
theta_dot0 = st.sidebar.number_input("Initial d(theta)/dt", value=0.0)
dt = st.sidebar.number_input("dt", value=0.1, format="%.4f")
g = 9.81
L = 1.0

# ****************************************
# Session State Initialization
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running

if 'theta_history' not in st.session_state:
    st.session_state.theta_history = [theta0]
    st.session_state.t_history = [0.0]
    st.session_state.theta = theta0
    st.session_state.theta_dot = theta_dot0
    st.session_state.t = 0.0

# ****************************************
# UI Layout
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader("Pendulum Animation")
    animation_placeholder = st.empty()

with col2:
    st.subheader("Theta vs. Time")
    plot_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running:
    st.session_state.theta_dot = st.session_state.theta_dot - (g / L) * np.sin(st.session_state.theta) * dt
    st.session_state.theta = st.session_state.theta + st.session_state.theta_dot * dt
    st.session_state.t = st.session_state.t + dt
    
    st.session_state.theta_history.append(st.session_state.theta)
    st.session_state.t_history.append(st.session_state.t)

    # Animation
    fig1, ax1 = plt.subplots()
    x = L * np.sin(st.session_state.theta)
    y = -L * np.cos(st.session_state.theta)
    ax1.plot([0, x], [0, y], 'o-')
    ax1.set_xlim(-1.2, 1.2)
    ax1.set_ylim(-1.2, 1.2)
    ax1.set_aspect('equal', adjustable='box')
    animation_placeholder.pyplot(fig1)
    plt.close(fig1)

    # Plot
    fig2, ax2 = plt.subplots()
    ax2.plot(st.session_state.t_history, st.session_state.theta_history)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Theta (radians)")
    plot_placeholder.pyplot(fig2)
    plt.close(fig2)
    
    time.sleep(0.05)
