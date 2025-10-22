import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Raster Frame Test")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
nx = st.sidebar.slider("Grid width (nx)", 32, 512, 256, 16)
ny = st.sidebar.slider("Grid height (ny)", 32, 512, 256, 16)
xmin = st.sidebar.number_input("x min", -20.0, 0.0, -10.0, 1.0)
xmax = st.sidebar.number_input("x max", 0.0, 20.0, 10.0, 1.0)
ymin = st.sidebar.number_input("y min", -20.0, 0.0, -10.0, 1.0)
ymax = st.sidebar.number_input("y max", 0.0, 20.0, 10.0, 1.0)

# ****************************************
# [Data Generation]
# ****************************************
# Use a button to control data generation
if 'data' not in st.session_state or st.sidebar.button("Generate New Data"):
    st.session_state.data = np.random.randint(0, 256, size=(ny, nx))

# ****************************************
# [Plotting]
# ****************************************
st.subheader("Random Raster Data")

fig, ax = plt.subplots()
im = ax.imshow(st.session_state.data, extent=(xmin, xmax, ymin, ymax), cmap='viridis', origin='lower')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Raster Frame")
fig.colorbar(im, ax=ax)

st.pyplot(fig)
