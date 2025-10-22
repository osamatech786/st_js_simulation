import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Falling Particle ODE", layout="wide")
st.title("🍂 Falling Particle ODE Solver")
st.write("This app simulates a falling particle using an ODE solver.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
y0 = st.sidebar.number_input("Initial y", value=10.0)
v0 = st.sidebar.number_input("Initial v", value=0.0)
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")

g = 9.81

# ****************************************
# Simulation Logic
# ****************************************
if st.sidebar.button("Run Simulation"):
    y = y0
    v = v0
    t = 0.0
    
    y_history = [y0]
    v_history = [v0]
    t_history = [0.0]

    while y > 0:
        v = v - g * dt
        y = y + v * dt
        t = t + dt
        
        y_history.append(y)
        v_history.append(v)
        t_history.append(t)

    st.subheader("Results")
    st.write(f"Final time = {t:.4f}")
    st.write(f"y = {y:.4f}, v = {v:.4f}")

    st.subheader("Data")
    st.dataframe({'Time (s)': t_history, 'Position (m)': y_history, 'Velocity (m/s)': v_history})

    st.subheader("Plots")
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(t_history, y_history)
    ax1.set_ylabel("Position (m)")
    ax2.plot(t_history, v_history)
    ax2.set_ylabel("Velocity (m/s)")
    ax2.set_xlabel("Time (s)")
    st.pyplot(fig)
