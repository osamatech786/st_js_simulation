import streamlit as st
import numpy as np

st.set_page_config(layout="centered")

st.title("PBC Test App")

# ****************************************
# [Simulation Parameters]
# ****************************************
st.sidebar.header("Simulation Parameters")
x = st.sidebar.number_input("Position (x)", -20.0, 20.0, -10.0, 0.1)
L = st.sidebar.number_input("Length (L)", 0.1, 20.0, 3.0, 0.1)

# ****************************************
# [PBC Functions]
# ****************************************
def pbc_position(x, length):
    """
    Calculates the position within the periodic boundary.
    """
    return x - length * np.floor(x / length)

def pbc_separation(x, length):
    """
    Calculates the separation using periodic boundary conditions.
    """
    return x - length * np.round(x / length)

# ****************************************
# [Calculation and Display]
# ****************************************
st.subheader("PBC Calculations")

if st.sidebar.button("Calculate"):
    position_new = pbc_position(x, L)
    separation_new = pbc_separation(x, L)

    st.write(f"**Position new:** {position_new:.4f}")
    st.write(f"**Separation new:** {separation_new:.4f}")
