import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Nuclear Decay Simulation", layout="wide")
st.title("Nuclear Decay Simulation")
st.write("This app simulates nuclear decay and plots the average number of unstable nuclei over time.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
n0 = st.sidebar.number_input("Initial number of unstable nuclei", value=1000, step=100)
p = st.sidebar.number_input("Decay probability", value=0.01, format="%.4f")
t_max = st.sidebar.number_input("Maximum time to collect data", value=100, step=10)
n_trials = st.sidebar.number_input("Number of trials", value=100, step=10)

# ****************************************
# Simulation Logic
# ****************************************
if st.sidebar.button("Run Simulation"):
    
    n_history = np.zeros(t_max + 1)

    for _ in range(n_trials):
        n_unstable = n0
        for t in range(t_max + 1):
            n_history[t] += n_unstable
            decayed_this_step = np.sum(np.random.rand(n_unstable) < p)
            n_unstable -= decayed_this_step
            
    n_average = n_history / n_trials

    # ****************************************
    # Display Results
    # ****************************************
    st.subheader("Average Number of Unstable Nuclei vs. Time")
    fig, ax = plt.subplots()
    ax.plot(range(t_max + 1), n_average, label="Simulation")
    
    # Analytical solution for comparison
    t_analytical = np.linspace(0, t_max, 200)
    n_analytical = n0 * np.exp(-p * t_analytical)
    ax.plot(t_analytical, n_analytical, '--', label="Analytical")
    
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of unstable nuclei")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Data")
    st.dataframe({'Time': range(t_max + 1), 'Average N': n_average})
