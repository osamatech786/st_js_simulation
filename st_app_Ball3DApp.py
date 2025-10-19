import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.set_page_config(page_title="3D Bouncing Ball Simulation", layout="wide")
st.title("🏀 3D Bouncing Ball Simulation")
st.write("This tool simulates a bouncing ball in 3D, based on the Java Ball3DApp.")

st.sidebar.header("Simulation Parameters")
z0 = st.sidebar.number_input("Initial Height (z₀) [m]", value=9.0, step=0.5)
vz0 = st.sidebar.number_input("Initial Velocity (vz₀) [m/s]", value=0.0, step=0.5)
dt = st.sidebar.number_input("Time Step (Δt) [s]", value=0.1, step=0.01, min_value=1e-6, format="%.4f")
n_steps = st.sidebar.number_input("Number of Steps (n)", value=100, step=10, min_value=1)
g = 9.8  # Gravity

def simulate_ball(z0, vz0, dt, n_steps):
    time = np.zeros(n_steps + 1)
    z = np.zeros(n_steps + 1)
    vz = np.zeros(n_steps + 1)

    time[0], z[0], vz[0] = 0.0, z0, vz0

    for i in range(n_steps):
        z[i+1] = z[i] + vz[i]*dt - 0.5*g*dt*dt
        vz[i+1] = vz[i] - g*dt
        time[i+1] = time[i] + dt

        if z[i+1] < 1 and vz[i+1] < 0:
            vz[i+1] = -vz[i+1]
            
    return time, z, vz

time, z, vz = simulate_ball(z0, vz0, dt, int(n_steps))

col1, col2 = st.columns(2)

with col1:
    st.subheader("3D Visualization")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Ball position
    ax.scatter(0, 0, z[-1], c='b', marker='o', s=100, label='Ball')

    # Box
    box_x = [-2, 2, 2, -2, -2]
    box_y = [-2, -2, 2, 2, -2]
    box_z = [0, 0, 0, 0, 0]
    ax.plot(box_x, box_y, box_z, color='r')

    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([0, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    st.pyplot(fig, clear_figure=True)

with col2:
    st.subheader("z(t) and vz(t)")
    fig2, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(time, z, marker='o', linestyle='-')
    ax1.set_ylabel('z [m]')
    ax2.plot(time, vz, marker='o', linestyle='-')
    ax2.set_xlabel('t [s]')
    ax2.set_ylabel('vz [m/s]')
    st.pyplot(fig2, clear_figure=True)

st.subheader("Simulation Data")
st.dataframe({'Time [s]': time, 'Position (z) [m]': z, 'Velocity (vz) [m/s]': vz})
