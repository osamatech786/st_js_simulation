import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("2D Scalar Field Visualizer")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
nx = st.sidebar.slider("Grid width (nx)", 8, 128, 16, 4)
ny = st.sidebar.slider("Grid height (ny)", 8, 128, 16, 4)
xmin = st.sidebar.number_input("x min", -20.0, 0.0, -10.0, 1.0)
xmax = st.sidebar.number_input("x max", 0.0, 20.0, 10.0, 1.0)
ymin = st.sidebar.number_input("y min", -20.0, 0.0, -10.0, 1.0)
ymax = st.sidebar.number_input("y max", 0.0, 20.0, 10.0, 1.0)
function_str = st.sidebar.text_input("Function f(x, y)", "x * y")

# ****************************************
# [Data Generation]
# ****************************************
x_vals = np.linspace(xmin, xmax, nx)
y_vals = np.linspace(ymin, ymax, ny)
x, y = np.meshgrid(x_vals, y_vals)

try:
    # Safe evaluation of the user-provided function string
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
    data = eval(function_str, {"__builtins__": {}}, safe_dict)
except Exception as e:
    st.error(f"Error evaluating function: {e}")
    st.stop()

# ****************************************
# [Plotting]
# ****************************************
st.subheader("Scalar Field Plot")

fig, ax = plt.subplots()
im = ax.imshow(data, extent=(xmin, xmax, ymin, ymax), cmap='viridis', origin='lower')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"Scalar Field of f(x, y) = {function_str}")
fig.colorbar(im, ax=ax, label="Value")

st.pyplot(fig)
