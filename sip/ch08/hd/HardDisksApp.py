import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from HardDisks import HardDisks

st.title("Hard Disks Simulation")

# Sidebar controls
st.sidebar.header("Simulation Controls")
N = st.sidebar.slider("Number of Particles (N)", 4, 100, 16)
Lx = st.sidebar.slider("Box Width (Lx)", 4.0, 20.0, 8.0)
Ly = st.sidebar.slider("Box Height (Ly)", 4.0, 20.0, 8.0)
config = st.sidebar.selectbox("Initial Configuration", ["regular", "random"])

# Initialize simulation
if 'hd' not in st.session_state:
    st.session_state.hd = HardDisks(N, Lx, Ly)
    st.session_state.hd.initialize(config)

hd = st.session_state.hd

# Main area for plots
fig, ax = plt.subplots()
pressure_fig, pressure_ax = plt.subplots()
pressure_data = st.empty()
display = st.empty()

# Simulation loop
if st.sidebar.button("Run Simulation"):
    pressure_ax.set_xlabel("Time")
    pressure_ax.set_ylabel("PA/NkT")
    pressure_ax.set_title("Pressure")
    
    time_to_plot = 1
    while True:
        while hd.t < time_to_plot:
            hd.step()
        
        time_to_plot += 1
        
        # Update pressure plot
        pressure_ax.plot(hd.t, hd.pressure(), 'bo')
        pressure_data.pyplot(pressure_fig)
        
        # Update display
        hd.draw(ax)
        display.pyplot(fig)
        
        if hd.number_of_collisions > 5000: # Stop condition
            break

if st.sidebar.button("Reset"):
    st.session_state.hd = HardDisks(N, Lx, Ly)
    st.session_state.hd.initialize(config)
    st.rerun()
