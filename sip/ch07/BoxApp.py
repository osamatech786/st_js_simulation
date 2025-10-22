import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Particles in a Box", layout="wide")
st.title("Particles in a Partitioned Box")
st.write("This app simulates the approach to equilibrium for particles in a partitioned box.")

# ****************************************
# Parameters and Session State
# ****************************************
st.sidebar.header("Parameters")
n_particles = st.sidebar.number_input("Number of particles", value=64, step=1)

if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running
    st.session_state.particles = np.random.rand(n_particles, 2)
    st.session_state.particles[:, 0] *= 0.5 # Start all on the left side
    st.session_state.n_left_history = [n_particles]
    st.session_state.time_history = [0]
    st.session_state.time = 0

if 'particles' not in st.session_state:
    st.session_state.particles = np.random.rand(n_particles, 2)
    st.session_state.particles[:, 0] *= 0.5 # Start all on the left side
    st.session_state.n_left_history = [n_particles]
    st.session_state.time_history = [0]
    st.session_state.time = 0

# ****************************************
# UI Layout
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader("Particle Positions")
    plot_placeholder = st.empty()

with col2:
    st.subheader("Number of Particles on Left")
    data_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running:
    # Move a random particle
    particle_to_move = np.random.randint(n_particles)
    st.session_state.particles[particle_to_move] = np.random.rand(2)
    
    n_left = np.sum(st.session_state.particles[:, 0] < 0.5)
    st.session_state.time += 1
    
    st.session_state.n_left_history.append(n_left)
    st.session_state.time_history.append(st.session_state.time)

    # Update plots
    fig1, ax1 = plt.subplots()
    ax1.plot(st.session_state.particles[:, 0], st.session_state.particles[:, 1], 'o')
    ax1.axvline(0.5, color='r', linestyle='--')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    plot_placeholder.pyplot(fig1)
    plt.close(fig1)

    fig2, ax2 = plt.subplots()
    ax2.plot(st.session_state.time_history, st.session_state.n_left_history)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Number on Left")
    data_placeholder.pyplot(fig2)
    plt.close(fig2)
    
    time.sleep(0.01)
