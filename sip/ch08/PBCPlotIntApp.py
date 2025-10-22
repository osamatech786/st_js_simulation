import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")

st.title("PBC Plot Integer App")

# ****************************************
# [Simulation Parameters]
# ****************************************
st.sidebar.header("Simulation Parameters")
L = st.sidebar.slider("Length (L)", 1, 20, 6, 1)
xmin = st.sidebar.number_input("x min", -40, 0, -20, 1)
xmax = st.sidebar.number_input("x max", 0, 40, 20, 1)

# ****************************************
# [PBC Function]
# ****************************************
def pbc_separation(x, length):
    """
    Calculates the separation using periodic boundary conditions,
    mimicking Java's Math.round behavior.
    """
    return x - length * np.floor(x / length + 0.5)

# ****************************************
# [Data Generation]
# ****************************************
x_values = np.arange(xmin, xmax + 1, 1)
y_values = pbc_separation(x_values, L)

data = pd.DataFrame({
    'x': x_values,
    'pbc': y_values
})

# ****************************************
# [Plotting]
# ****************************************
st.subheader("PBC Demo")

fig, ax = plt.subplots()
ax.plot(data['x'], data['pbc'], 'o-')
ax.set_xlabel("x")
ax.set_ylabel("pbc")
ax.set_title("PBC Demo")
ax.grid(True)

st.pyplot(fig)

st.subheader("Raw Data")
st.write(data)
