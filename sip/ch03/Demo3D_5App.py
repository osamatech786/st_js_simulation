import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

st.set_page_config(page_title="3D Demo 5", layout="wide")
st.title("🏀 Ball in a Box")
st.write("A simulation of a ball bouncing in a box, converted from Java.")

# ****************************************
# Simulation Parameters and Initialization
# ****************************************
ball_radius = 0.05
min_val, max_val = -1.0, 1.0
dt = 0.1

x = (max_val - min_val) * (np.random.rand() - 0.5)
y = (max_val - min_val) * (np.random.rand() - 0.5)
z = (max_val - min_val) * (np.random.rand() - 0.5)
vx = (max_val - min_val) * (np.random.rand() - 0.5)
vy = (max_val - min_val) * (np.random.rand() - 0.5)
vz = (max_val - min_val) * (np.random.rand() - 0.5)

# ****************************************
# 3D Scene Setup
# ****************************************
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Box
xx = [min_val, max_val, max_val, min_val, min_val]
yy = [min_val, min_val, max_val, max_val, min_val]
ax.plot(xx, yy, [min_val]*5, color="gray")
ax.plot(xx, yy, [max_val]*5, color="gray")
for i in range(4):
    ax.plot([xx[i], xx[i]], [yy[i], yy[i]], [min_val, max_val], color="gray")

trail_points = []

ax.set_xlim([min_val, max_val])
ax.set_ylim([min_val, max_val])
ax.set_zlim([min_val, max_val])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# ****************************************
# Animation Loop
# ****************************************
plot_placeholder = st.empty()

while True:
    x += vx * dt
    y += vy * dt
    z += vz * dt

    if x < min_val or x > max_val:
        vx = -vx
    if y < min_val or y > max_val:
        vy = -vy
    if z < min_val or z > max_val:
        vz = -vz

    trail_points.append((x, y, z))
    if len(trail_points) > 30:
        trail_points.pop(0)

    ax.cla()

    # Box
    xx = [min_val, max_val, max_val, min_val, min_val]
    yy = [min_val, min_val, max_val, max_val, min_val]
    ax.plot(xx, yy, [min_val]*5, color="gray")
    ax.plot(xx, yy, [max_val]*5, color="gray")
    for i in range(4):
        ax.plot([xx[i], xx[i]], [yy[i], yy[i]], [min_val, max_val], color="gray")

    # Ball
    ax.scatter(x, y, z, c='b', marker='o', s=100)

    # Trail
    if len(trail_points) > 1:
        trail_x, trail_y, trail_z = zip(*trail_points)
        ax.plot(trail_x, trail_y, trail_z, color='gray', linestyle='-')

    ax.set_xlim([min_val, max_val])
    ax.set_ylim([min_val, max_val])
    ax.set_zlim([min_val, max_val])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plot_placeholder.pyplot(fig)
    time.sleep(0.05)
