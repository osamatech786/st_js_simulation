import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Iterate Map", layout="wide")
st.title("Iterate Map")
st.write("This app calculates and plots multiple trajectories of the logistic equation.")

# ****************************************
# Session State and Parameters
# ****************************************
if 'trajectories' not in st.session_state:
    st.session_state.trajectories = []

st.sidebar.header("Parameters")
r = st.sidebar.number_input("r", value=0.2)
x0 = st.sidebar.number_input("x", value=0.6)
iterations = st.sidebar.number_input("iterations", value=50, step=1)

# ****************************************
# Logistic Map Function
# ****************************************
def logistic_map(r, x):
    return 4 * r * x * (1 - x)

# ****************************************
# Main Logic and Display
# ****************************************
if st.sidebar.button("Add Trajectory"):
    x = x0
    trajectory = []
    for _ in range(iterations + 1):
        trajectory.append(x)
        x = logistic_map(r, x)
    st.session_state.trajectories.append(trajectory)

if st.sidebar.button("Clear Trajectories"):
    st.session_state.trajectories = []

st.subheader("Trajectories")
fig, ax = plt.subplots()
for i, trajectory in enumerate(st.session_state.trajectories):
    ax.plot(range(len(trajectory)), trajectory, 'o-', label=f"Trajectory {i+1}")

ax.set_xlabel("Iterations")
ax.set_ylabel("x")
if st.session_state.trajectories:
    ax.legend()
st.pyplot(fig)
