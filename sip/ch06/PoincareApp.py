import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Poincaré Section of a Damped Driven Pendulum", layout="wide")
st.title("Poincaré Section of a Damped Driven Pendulum")
st.write("This app plots a phase diagram and a Poincaré map for the damped, driven pendulum.")

# ****************************************
# Parameters
# ****************************************
st.sidebar.header("Parameters")
theta0 = st.sidebar.number_input("theta", value=0.2)
omega0 = st.sidebar.number_input("angular velocity", value=0.6)
gamma = st.sidebar.number_input("gamma", value=0.2)
A = st.sidebar.number_input("A", value=0.85)
n_steps = st.sidebar.number_input("Number of Steps", value=10000, step=100)

omega_drive = 2.0
dt = np.pi / 100

# ****************************************
# Simulation Logic and Display
# ****************************************
if st.sidebar.button("Run Simulation"):
    theta = theta0
    omega = omega0
    t = 0
    
    theta_history = []
    omega_history = []
    poincare_theta = []
    poincare_omega = []

    for i in range(n_steps):
        alpha = -np.sin(theta) - gamma * omega + A * np.cos(omega_drive * t)
        omega += alpha * dt
        theta += omega * dt
        t += dt
        
        if theta > np.pi:
            theta -= 2 * np.pi
        elif theta < -np.pi:
            theta += 2 * np.pi
            
        theta_history.append(theta)
        omega_history.append(omega)
        
        if i % 100 == 0:
            poincare_theta.append(theta)
            poincare_omega.append(omega)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Phase Space")
        fig1, ax1 = plt.subplots()
        ax1.plot(theta_history, omega_history, ',')
        ax1.set_xlabel("theta")
        ax1.set_ylabel("angular velocity")
        st.pyplot(fig1)
        
    with col2:
        st.subheader("Poincaré Section")
        fig2, ax2 = plt.subplots()
        ax2.plot(poincare_theta, poincare_omega, 'r.')
        ax2.set_xlabel("theta")
        ax2.set_ylabel("angular velocity")
        st.pyplot(fig2)
