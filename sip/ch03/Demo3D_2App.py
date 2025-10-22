import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

st.set_page_config(page_title="3D Demo 2", layout="wide")
st.title("🛰️ 3D Demo 2")
st.write("A demonstration of an OSP 3D group, converted from Java.")

# ****************************************
# 3D Scene Setup
# ****************************************
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Planet
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x_planet = 5 * np.cos(u)*np.sin(v)
y_planet = 5 * np.sin(u)*np.sin(v)
z_planet = 5 * np.cos(v)
ax.plot_surface(x_planet, y_planet, z_planet, color='b')

# Satellites
satellites = []
for i in range(10):
    alpha = np.random.rand() * np.pi * 2.0
    beta = -np.pi * 0.5 + np.random.rand() * np.pi
    x = 7 * np.cos(alpha) * np.cos(beta)
    y = 7 * np.sin(alpha) * np.cos(beta)
    z = 7 * np.sin(beta)
    satellites.append(ax.scatter(x, y, z, c='r', marker='o'))

ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_zlim([-10, 10])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ****************************************
# Animation Loop
# ****************************************
plot_placeholder = st.empty()

theta = 0
while True:
    theta += np.pi / 20
    
    # This is a simplified rotation around the Z axis
    # A more complex rotation like in the Java code would require more complex math
    ax.view_init(elev=30, azim=theta * 180 / np.pi)
    
    plot_placeholder.pyplot(fig)
    time.sleep(0.1)
