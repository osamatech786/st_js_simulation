import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(layout="centered")

st.title("PBC Plot App")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
L = st.sidebar.slider("Length (L)", 1.0, 10.0, 4.0, 0.1)
xmin = st.sidebar.number_input("x min", -20.0, 0.0, -10.0, 0.1)
xmax = st.sidebar.number_input("x max", 0.0, 20.0, 10.0, 0.1)
dx = st.sidebar.number_input("dx", 0.01, 1.0, 0.02, 0.01)

# ****************************************
# PBC Function
# ****************************************
def pbc_separation(x, length):
    """
    Calculates the separation using periodic boundary conditions,
    mimicking Java's Math.round behavior.
    """
    return x - length * np.floor(x / length + 0.5)

# ****************************************
# Data Generation
# ****************************************
x_values = np.arange(xmin, xmax + dx, dx)
y_values = pbc_separation(x_values, L)

data = pd.DataFrame({
    'x': x_values,
    'pbc': y_values
})

# ****************************************
# Plotting
# ****************************************
st.subheader("PBC Demo")

fig, ax = plt.subplots()
ax.plot(data['x'], data['pbc'])
ax.set_xlabel("x")
ax.set_ylabel("pbc")
ax.set_title("PBC Demo")
ax.grid(True)

st.pyplot(fig)

st.subheader("Raw Data")
st.write(data)
