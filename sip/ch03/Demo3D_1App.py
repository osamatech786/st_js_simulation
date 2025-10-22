import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

st.set_page_config(page_title="3D Demo 1", layout="wide")
st.title("🎨 3D Demo 1")
st.write("A demonstration of 3D Elements, converted from Java.")

# ****************************************
# 3D Scene Setup
# ****************************************
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# ****************************************
# 3D Objects
# ****************************************
# Cylinder 1
u = np.linspace(0, 2 * np.pi, 50)
h = np.linspace(-0.4, 0.4, 20)
x = np.outer(0.2 * np.sin(u), np.ones(len(h)))
y = np.outer(0.2 * np.cos(u), np.ones(len(h)))
z = np.outer(np.ones(len(u)), h)
ax.plot_surface(x, y, z, color='b')

# Cylinder 2
x2 = np.outer(0.1 * np.sin(u), np.ones(len(h))) + 0.8
y2 = np.outer(0.1 * np.cos(u), np.ones(len(h))) - 0.8
z2 = np.outer(np.ones(len(u)), h)
ax.plot_surface(x2, y2, z2, color='b')

# Sphere 1
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x3 = 0.2 * np.cos(u)*np.sin(v) - 0.8
y3 = 0.2 * np.sin(u)*np.sin(v) + 0.8
z3 = 0.2 * np.cos(v)
ax.plot_surface(x3, y3, z3, color='g')

# Cone 1
u = np.linspace(0, 2 * np.pi, 50)
z4 = np.linspace(0, 0.8, 50)
x4 = np.outer(0.2 * (1 - z4/0.8) * np.sin(u), np.ones(len(z4))) - 0.8
y4 = np.outer(0.2 * (1 - z4/0.8) * np.cos(u), np.ones(len(z4))) - 0.8
ax.plot_surface(x4, y4, z4, color='pink')

# Surface 1
nu, nv = 16, 32
u = np.linspace(0, 2, nu)
v = np.linspace(0, 2, nv)
U, V = np.meshgrid(u, v)
X = U
Y = V
Z = np.cos(3.0 * (Y - 1)) * (X - 1) * (1.5 - X) / 2.0
ax.plot_surface(X-1, Y-1, Z-1, color='r', rstride=1, cstride=1, cmap='viridis')

# ****************************************
# Plotting and Display
# ****************************************
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=30, azim=20)

st.pyplot(fig)
