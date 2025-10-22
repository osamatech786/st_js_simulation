import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Three-Body Problem", layout="wide")
st.title("🔭 Three-Body Problem")
st.write("This app simulates the three-body problem with different initial conditions.")

# ****************************************
# Simulation Parameters and Initial Conditions
# ****************************************
st.sidebar.header("Simulation Parameters")
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")
initial_conditions = st.sidebar.selectbox(
    "Initial Conditions",
    ("MONTGOMERY", "EULER", "LAGRANGE")
)

sn = np.sin(np.pi/3)
half = np.cos(np.pi/3)
x1 = 0.97000436
v1 = 0.93240737/2
y1 = 0.24308753
v2 = 0.86473146/2
v = 0.8

conditions = {
    "EULER": [0, 0, 0, 0, 1, 0, 0, v, -1, 0, 0, -v, 0],
    "LAGRANGE": [1, 0, 0, v, -half, -v*sn, sn, -v*half, -half, v*sn, -sn, -v*half, 0],
    "MONTGOMERY": [x1, v1, -y1, v2, -x1, v1, y1, v2, 0, -2*v1, 0, -2*v2, 0]
}

state = np.array(conditions[initial_conditions])

# ****************************************
# Session State Initialization
# ****************************************
if 'running' not in st.session_state:
    st.session_state.running = False

if st.sidebar.button("Start/Stop"):
    st.session_state.running = not st.session_state.running
    st.session_state.state = state
    st.session_state.history = [state.copy()]

if 'history' not in st.session_state:
    st.session_state.history = [state.copy()]

# ****************************************
# UI Layout
# ****************************************
st.subheader("Orbits")
plot_placeholder = st.empty()

# ****************************************
# Simulation Loop
# ****************************************
while st.session_state.running:
    s = st.session_state.state
    r12 = np.sqrt((s[0]-s[4])**2 + (s[2]-s[6])**2)
    r13 = np.sqrt((s[0]-s[8])**2 + (s[2]-s[10])**2)
    r23 = np.sqrt((s[4]-s[8])**2 + (s[6]-s[10])**2)
    
    ax1 = -(s[0]-s[4])/r12**3 - (s[0]-s[8])/r13**3
    ay1 = -(s[2]-s[6])/r12**3 - (s[2]-s[10])/r13**3
    ax2 = -(s[4]-s[0])/r12**3 - (s[4]-s[8])/r23**3
    ay2 = -(s[6]-s[2])/r12**3 - (s[6]-s[10])/r23**3
    ax3 = -(s[8]-s[0])/r13**3 - (s[8]-s[4])/r23**3
    ay3 = -(s[10]-s[2])/r13**3 - (s[10]-s[6])/r23**3
    
    s[1] += ax1 * dt
    s[3] += ay1 * dt
    s[5] += ax2 * dt
    s[7] += ay2 * dt
    s[9] += ax3 * dt
    s[11] += ay3 * dt
    
    s[0] += s[1] * dt
    s[2] += s[3] * dt
    s[4] += s[5] * dt
    s[6] += s[7] * dt
    s[8] += s[9] * dt
    s[10] += s[11] * dt
    s[12] += dt
    
    st.session_state.history.append(s.copy())

    fig, ax = plt.subplots()
    history = np.array(st.session_state.history)
    ax.plot(history[:, 0], history[:, 2], 'r-')
    ax.plot(history[:, 4], history[:, 6], 'g-')
    ax.plot(history[:, 8], history[:, 10], 'b-')
    ax.plot(s[0], s[2], 'ro')
    ax.plot(s[4], s[6], 'go')
    ax.plot(s[8], s[10], 'bo')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal', adjustable='box')
    plot_placeholder.pyplot(fig)
    plt.close(fig)
    
    time.sleep(0.01)
