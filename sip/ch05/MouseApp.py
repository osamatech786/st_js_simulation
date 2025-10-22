import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Mouse App", layout="wide")
st.title("🖱️ Mouse App (Simplified)")
st.write("This app demonstrates a simplified version of interactive plotting in Streamlit.")
st.write("Streamlit does not support low-level mouse events like 'pressed' or 'dragged' on plots.")

# ****************************************
# Session State and Plot Setup
# ****************************************
# A simple interactive plot where you can add points by clicking
if 'points' not in st.session_state:
    st.session_state.points = []

st.write("Click on the plot to add points.")

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# ****************************************
# User Interaction and Display
# ****************************************
if st.button("Add a random point"):
    st.session_state.points.append(np.random.rand(2) * 10)

if st.button("Clear points"):
    st.session_state.points = []

if st.session_state.points:
    x, y = zip(*st.session_state.points)
    ax.scatter(x, y)

st.pyplot(fig)
