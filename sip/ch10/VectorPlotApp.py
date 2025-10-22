import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("2D Vector Field Plotter")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
nx = st.sidebar.slider("Grid width (nx)", 5, 30, 15, 1)
ny = st.sidebar.slider("Grid height (ny)", 5, 30, 15, 1)
xmin = st.sidebar.number_input("x min", -10.0, 0.0, -2.0, 0.1)
xmax = st.sidebar.number_input("x max", 0.0, 10.0, 2.0, 0.1)
ymin = st.sidebar.number_input("y min", -10.0, 0.0, -2.0, 0.1)
ymax = st.sidebar.number_input("y max", 0.0, 10.0, 2.0, 0.1)

st.sidebar.subheader("Vector Field Components")
fx_str = st.sidebar.text_input("Fx(x, y)", "x / (x**2 + y**2)**1.5")
fy_str = st.sidebar.text_input("Fy(x, y)", "y / (x**2 + y**2)**1.5")

# ****************************************
# [Data Generation]
# ****************************************
x_vals = np.linspace(xmin, xmax, nx)
y_vals = np.linspace(ymin, ymax, ny)
x, y = np.meshgrid(x_vals, y_vals)

# Avoid division by zero at the origin
r_squared = x**2 + y**2
r_squared[r_squared == 0] = 1e-9

try:
    # Safe evaluation of the user-provided function strings
    safe_dict = {
        'x': x,
        'y': y,
        'np': np,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'exp': np.exp,
        'sqrt': np.sqrt,
        'pi': np.pi
    }
    # Add r_squared to the context for convenience
    safe_dict['r_squared'] = r_squared
    
    fx = eval(fx_str, {"__builtins__": {}}, safe_dict)
    fy = eval(fy_str, {"__builtins__": {}}, safe_dict)
except Exception as e:
    st.error(f"Error evaluating function: {e}")
    st.stop()

# ****************************************
# [Plotting]
# ****************************************
st.subheader("Vector Field Plot")

fig, ax = plt.subplots(figsize=(10, 10))
magnitude = np.sqrt(fx**2 + fy**2)

quiver = ax.quiver(x, y, fx, fy, magnitude, cmap='viridis')
fig.colorbar(quiver, ax=ax, label="Magnitude")

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Vector Field")
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect('equal', adjustable='box')
ax.grid(True)

st.pyplot(fig)
