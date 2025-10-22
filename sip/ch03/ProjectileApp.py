import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Projectile Motion", layout="wide")
st.title("🚀 Projectile Motion")
st.write("This app simulates the motion of a projectile.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
x0 = st.sidebar.number_input("Initial x", value=0.0)
vx0 = st.sidebar.number_input("Initial vx", value=10.0)
y0 = st.sidebar.number_input("Initial y", value=0.0)
vy0 = st.sidebar.number_input("Initial vy", value=10.0)
dt = st.sidebar.number_input("dt", value=0.01, format="%.4f")

g = 9.81

# ****************************************
# Simulation Logic
# ****************************************
if st.sidebar.button("Run Simulation"):
    x = x0
    y = y0
    vx = vx0
    vy = vy0
    t = 0.0
    
    x_history = [x0]
    y_history = [y0]
    t_history = [0.0]

    while y >= 0:
        vx = vx
        vy = vy - g * dt
        x = x + vx * dt
        y = y + vy * dt
        t = t + dt
        
        x_history.append(x)
        y_history.append(y)
        t_history.append(t)

    st.subheader("Trajectory")
    fig1, ax1 = plt.subplots()
    ax1.plot(x_history, y_history)
    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("y (m)")
    st.pyplot(fig1)

    st.subheader("Position vs. Time")
    fig2, (ax2, ax3) = plt.subplots(2, 1, sharex=True)
    ax2.plot(t_history, x_history)
    ax2.set_ylabel("x (m)")
    ax3.plot(t_history, y_history)
    ax3.set_ylabel("y (m)")
    ax3.set_xlabel("Time (s)")
    st.pyplot(fig2)

    st.subheader("Data")
    st.dataframe({'Time (s)': t_history, 'x (m)': x_history, 'y (m)': y_history})
