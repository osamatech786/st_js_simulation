import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="1D Random Walk", layout="wide")
st.title("1D Random Walk Simulation")
st.write("This app simulates random walkers in one dimension.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
p_right = st.sidebar.slider("Probability p of step to right", 0.0, 1.0, 0.5)
n_steps = st.sidebar.number_input("Number of steps N", value=100, step=10)
n_trials = st.sidebar.number_input("Number of trials", value=1000, step=100)

# ****************************************
# Simulation Logic
# ****************************************
if st.sidebar.button("Run Simulation"):
    final_positions = []
    x_accum = np.zeros(n_steps + 1)
    x2_accum = np.zeros(n_steps + 1)

    for _ in range(n_trials):
        position = 0
        x_accum[0] += position
        x2_accum[0] += position**2
        for i in range(n_steps):
            if np.random.rand() < p_right:
                position += 1
            else:
                position -= 1
            x_accum[i+1] += position
            x2_accum[i+1] += position**2
        final_positions.append(position)

    x_avg = x_accum / n_trials
    x2_avg = x2_accum / n_trials
    variance = x2_avg - x_avg**2

    # ****************************************
    # Display Results
    # ****************************************
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Averages")
        fig1, ax1 = plt.subplots()
        ax1.plot(range(n_steps + 1), x_avg, label="<x>")
        ax1.plot(range(n_steps + 1), variance, label="<x^2> - <x>^2")
        ax1.set_xlabel("Time")
        ax1.set_ylabel("Value")
        ax1.legend()
        st.pyplot(fig1)

    with col2:
        st.subheader("Final Position Distribution")
        fig2, ax2 = plt.subplots()
        ax2.hist(final_positions, bins=20, density=True)
        ax2.set_xlabel("Final Position")
        ax2.set_ylabel("Probability")
        st.pyplot(fig2)
