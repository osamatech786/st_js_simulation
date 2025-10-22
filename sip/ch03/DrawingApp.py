import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Drawing App", layout="wide")
st.title("🎨 Drawing App")
st.write("This app allows you to draw rectangles on a canvas.")

# ****************************************
# Session State Initialization
# ****************************************
if 'rectangles' not in st.session_state:
    st.session_state.rectangles = []

# ****************************************
# User Inputs
# ****************************************
st.sidebar.header("Rectangle Parameters")
xleft = st.sidebar.number_input("X Left", value=1, step=1)
ytop = st.sidebar.number_input("Y Top", value=8, step=1)
width = st.sidebar.number_input("Width", value=2, step=1)
height = st.sidebar.number_input("Height", value=2, step=1)

if st.sidebar.button("Add Rectangle"):
    st.session_state.rectangles.append((xleft, ytop - height, width, height))

if st.sidebar.button("Clear Canvas"):
    st.session_state.rectangles = []

# ****************************************
# Drawing Canvas
# ****************************************
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect('equal', adjustable='box')

for rect in st.session_state.rectangles:
    ax.add_patch(patches.Rectangle((rect[0], rect[1]), rect[2], rect[3], fill=True))

st.pyplot(fig)
