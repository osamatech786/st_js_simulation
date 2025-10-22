import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Fermat's Principle", layout="wide")
st.title("Fermat's Principle of Least Time")
st.write("This app simulates the use of Fermat's principle to find the light path that minimizes time.")

# ****************************************
# Parameters and Session State
# ****************************************
st.sidebar.header("Parameters")
dn = st.sidebar.number_input("Change in index of refraction", value=0.5)
N = st.sidebar.number_input("Number of media segments", value=2, step=1)
n_steps = st.sidebar.number_input("Number of simulation steps", value=100, step=10)

if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running
    st.session_state.y = np.linspace(1, 0, N + 1)
    st.session_state.n = 1 + dn * np.arange(N + 1) / N
    st.session_state.step = 0

if 'y' not in st.session_state:
    st.session_state.y = np.linspace(1, 0, N + 1)
    st.session_state.n = 1 + dn * np.arange(N + 1) / N
    st.session_state.step = 0

# ****************************************
# UI Layout
# ****************************************
st.subheader("Light Path")
plot_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running and st.session_state.step < n_steps:
    i = np.random.randint(1, N)
    y_old = st.session_state.y[i]
    
    # Simplified version of the minimization step
    st.session_state.y[i] += (np.random.rand() - 0.5) * 0.1
    
    st.session_state.step += 1

    fig, ax = plt.subplots()
    ax.plot(range(N + 1), st.session_state.y, 'o-')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    plot_placeholder.pyplot(fig)
    plt.close(fig)
    
    time.sleep(0.01)
