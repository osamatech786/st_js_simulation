import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from LJParticles import LJParticles

st.title("Lennard-Jones Particles Simulation")

# Sidebar controls
st.sidebar.header("Simulation Controls")
nx = st.sidebar.slider("Particles per row (nx)", 2, 20, 8)
ny = st.sidebar.slider("Particles per column (ny)", 2, 20, 8)
initial_ke = st.sidebar.slider("Initial KE per particle", 0.1, 5.0, 1.0)
Lx = st.sidebar.slider("Box Width (Lx)", 10.0, 50.0, 20.0)
Ly = st.sidebar.slider("Box Height (Ly)", 10.0, 50.0, 15.0)
dt = st.sidebar.slider("Time step (dt)", 0.001, 0.1, 0.01)
config = st.sidebar.selectbox("Initial Configuration", ["rectangular", "triangular", "random"])

# Initialize simulation
if 'md' not in st.session_state:
    st.session_state.md = LJParticles(nx, ny, Lx, Ly, initial_ke, dt, config)
    st.session_state.md.initialize()

md = st.session_state.md

# Main area for plots
fig, ax = plt.subplots()
pressure_fig, pressure_ax = plt.subplots()
temp_fig, temp_ax = plt.subplots()
hist_fig, hist_ax = plt.subplots()

pressure_data = st.empty()
temp_data = st.empty()
hist_data = st.empty()
display = st.empty()

# Simulation loop
if st.sidebar.button("Run Simulation"):
    pressure_ax.set_xlabel("Time")
    pressure_ax.set_ylabel("PA/NkT")
    pressure_ax.set_title("Mean Pressure")
    
    temp_ax.set_xlabel("Time")
    temp_ax.set_ylabel("Temperature")
    temp_ax.set_title("Mean Temperature")
    
    hist_ax.set_xlabel("vx")
    hist_ax.set_ylabel("H(vx)")
    hist_ax.set_title("Velocity Histogram")

    x_velocity_histogram = []
    
    while True:
        md.step(x_velocity_histogram)
        
        # Update plots
        pressure_ax.plot(md.t, md.get_mean_pressure(), 'bo')
        pressure_data.pyplot(pressure_fig)
        
        temp_ax.plot(md.t, md.get_mean_temperature(), 'ro')
        temp_data.pyplot(temp_fig)
        
        hist_ax.clear()
        hist_ax.hist(x_velocity_histogram, bins=20)
        hist_data.pyplot(hist_fig)
        
        md.draw(ax)
        display.pyplot(fig)
        
        if md.steps > 1000: # Stop condition
            break

if st.sidebar.button("Reset"):
    st.session_state.md = LJParticles(nx, ny, Lx, Ly, initial_ke, dt, config)
    st.session_state.md.initialize()
    st.rerun()
