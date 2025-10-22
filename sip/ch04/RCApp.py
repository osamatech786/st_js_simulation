import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="RC Circuit Simulation", layout="wide")
st.title("🔌 RC Circuit Simulation")
st.write("This app simulates an RC circuit with a sinusoidal driving voltage.")

# ****************************************
# Circuit Parameters
# ****************************************
st.sidebar.header("Circuit Parameters")
r = st.sidebar.number_input("Resistance (R)", value=1.0)
c = st.sidebar.number_input("Capacitance (C)", value=1.0)
omega = st.sidebar.number_input("Angular Frequency (ω)", value=1.0)
dt = st.sidebar.number_input("Time Step (dt)", value=0.1, format="%.4f")
t_max = st.sidebar.number_input("Max Time", value=50.0)

# ****************************************
# Source Voltage Function
# ****************************************
def source_voltage(t, omega):
    return np.sin(omega * t)

# ****************************************
# Simulation Logic
# ****************************************
if st.sidebar.button("Run Simulation"):
    t = 0
    q = 0
    
    t_history = [0]
    q_history = [0]
    v_source_history = [source_voltage(0, omega)]

    while t < t_max:
        dq_dt = (source_voltage(t, omega) - q / c) / r
        q = q + dq_dt * dt
        t = t + dt
        
        t_history.append(t)
        q_history.append(q)
        v_source_history.append(source_voltage(t, omega))

    # ****************************************
    # Display Results
    # ****************************************
    st.subheader("Charge and Source Voltage vs. Time")
    fig, ax = plt.subplots()
    ax.plot(t_history, q_history, label="Charge (q)")
    ax.plot(t_history, v_source_history, label="Source Voltage (V)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Data")
    st.dataframe({'Time (s)': t_history, 'Charge (q)': q_history, 'Source Voltage (V)': v_source_history})
