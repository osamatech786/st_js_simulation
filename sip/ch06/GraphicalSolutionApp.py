import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Graphical Solution of the Logistic Map", layout="wide")
st.title("Graphical Solution of the Logistic Map")
st.write("This app presents a graphical solution to the logistic map.")

# ****************************************
# Parameters
# ****************************************
st.sidebar.header("Parameters")
r = st.sidebar.slider("r", 0.0, 1.0, 0.89)
x0 = st.sidebar.slider("Initial x", 0.0, 1.0, 0.2)
n_iterations = st.sidebar.slider("Iterations", 1, 100, 10)

# ****************************************
# Logistic Map Function
# ****************************************
def logistic_map(x, r):
    return 4 * r * x * (1 - x)

# ****************************************
# Plotting
# ****************************************
x_vals = np.linspace(0, 1, 400)
y_vals = logistic_map(x_vals, r)

fig, ax = plt.subplots(figsize=(8, 8))
ax.plot(x_vals, y_vals, label="f(x) = 4rx(1-x)")
ax.plot([0, 1], [0, 1], 'k--', label="y = x")

# Plot the trajectory
x = x0
for _ in range(n_iterations):
    y = logistic_map(x, r)
    ax.plot([x, x], [x, y], 'gray', linestyle='--')
    ax.plot([x, y], [y, y], 'gray', linestyle='--')
    x = y

ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend()
st.pyplot(fig)
