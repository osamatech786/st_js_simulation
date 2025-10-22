import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Bifurcation Diagram", layout="wide")
st.title("Bifurcation Diagram of the Logistic Map")
st.write("This app demonstrates chaos in the logistic equation by plotting the return map for different values of r.")

# ****************************************
# Simulation Parameters
# ****************************************
st.sidebar.header("Simulation Parameters")
r_initial = st.sidebar.number_input("Initial r", value=0.2)
dr = st.sidebar.number_input("dr", value=0.005, format="%.4f")
ntransient = st.sidebar.number_input("ntransient", value=200)
nplot = st.sidebar.number_input("nplot", value=50)
r_max = st.sidebar.number_input("Max r", value=1.0)

# ****************************************
# Logistic Map Function
# ****************************************
def logistic_map(x, r):
    return 4 * r * x * (1 - x)

# ****************************************
# Simulation Logic and Display
# ****************************************
if st.sidebar.button("Generate Diagram"):
    r_values = np.arange(r_initial, r_max, dr)
    x_values = []
    r_plot_values = []

    for r in r_values:
        x = 0.5
        for _ in range(ntransient):
            x = logistic_map(x, r)
        for _ in range(nplot):
            x = logistic_map(x, r)
            x_values.append(x)
            r_plot_values.append(r)

    st.subheader("Bifurcation Diagram")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(r_plot_values, x_values, ',k', alpha=0.25)
    ax.set_xlabel("r")
    ax.set_ylabel("x")
    st.pyplot(fig)
