import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

st.set_page_config(page_title="3D Demo 3", layout="wide")
st.title("🧊 3D Demo 3")
st.write("A demonstration of various 3D Elements, converted from Java.")

# ****************************************
# 3D Scene Setup
# ****************************************
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111, projection='3d')

# ****************************************
# 3D Objects
# ****************************************
# Arrow
ax.quiver(-0.5, -0.5, -1, 1, 0, 0, color='r')

# Trihedron
ax.quiver(0.5, 0.5, 1, 0.3, 0, 0, color='g')
ax.quiver(0.5, 0.5, 1, 0, 0.3, 0, color='g')
ax.quiver(0.5, 0.5, 1, 0, 0, 0.3, color='g')
ax.quiver(0.6, 0.6, 1.1, 0.4, 0, 0, color='r', linewidth=1.5)

# Box
def plot_cube(ax, center, size):
    x, y, z = center
    dx, dy, dz = size
    xx = [x - dx/2, x + dx/2, x + dx/2, x - dx/2, x - dx/2]
    yy = [y - dy/2, y - dy/2, y + dy/2, y + dy/2, y - dy/2]
    ax.plot(xx, yy, [z - dz/2]*5, color="b")
    ax.plot(xx, yy, [z + dz/2]*5, color="b")
    for i in range(4):
        ax.plot([xx[i], xx[i]], [yy[i], yy[i]], [z - dz/2, z + dz/2], color="b")

plot_cube(ax, (0.5, -0.5, -0.75), (0.5, 0.5, 0.3))

# Torus
nu, nv = 20, 15
R, r = 0.7, 0.2
u = np.linspace(0, 2 * np.pi, nu)
v = np.linspace(0, 2 * np.pi, nv)
u, v = np.meshgrid(u, v)
x = (R + r * np.cos(v)) * np.cos(u)
y = (R + r * np.cos(v)) * np.sin(u)
z = r * np.sin(v)
ax.plot_surface(x, y + 0.5, z + 0.5, color='c')

# Plane
x_plane = np.linspace(-1, 1, 5)
y_plane = np.linspace(-np.sqrt(2), np.sqrt(2), 5)
X_plane, Y_plane = np.meshgrid(x_plane, y_plane)
Z_plane = -Y_plane / np.sqrt(2)
ax.plot_surface(X_plane, Y_plane / np.sqrt(2), Z_plane, color=(0, 0, 1, 0.5))

# Cone
u_cone = np.linspace(0, 2 * np.pi, 50)
z_cone = np.linspace(0, 0.5, 50)
x_cone = np.outer(0.25 * (1 - z_cone/0.5), np.ones(len(z_cone))) * np.cos(u_cone) + 1
y_cone = np.outer(0.25 * (1 - z_cone/0.5), np.ones(len(z_cone))) * np.sin(u_cone)
ax.plot_surface(x_cone, y_cone, z_cone - 1 + 0.25, color='m')


ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ****************************************
# Animation Loop
# ****************************************
plot_placeholder = st.empty()

angle = 0
while True:
    angle += 5
    ax.view_init(elev=30, azim=angle)
    plot_placeholder.pyplot(fig)
    time.sleep(0.1)
