import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

st.set_page_config(page_title="3D Demo 4", layout="wide")
st.title("⚛️ 3D Demo 4")
st.write("A demonstration of particle motion simulation, converted from Java.")

# ****************************************
# Simulation Parameters
# ****************************************
num_electrons = 50
radius = 7.0

alphas = np.random.rand(num_electrons) * np.pi * 2.0
betas = -np.pi * 0.5 + np.random.rand(num_electrons) * np.pi

# ****************************************
# 3D Scene Setup
# ****************************************
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Nucleus
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x_nucleus = 1.5 * np.cos(u)*np.sin(v)
y_nucleus = 1.5 * np.sin(u)*np.sin(v)
z_nucleus = 1.5 * np.cos(v)
ax.plot_surface(x_nucleus, y_nucleus, z_nucleus, color='b')

# Electrons and Trails
electrons_scatter = ax.scatter([], [], [], c='r', marker='o')
trails = [ax.plot([], [], [], color='gray')[0] for _ in range(num_electrons)]
trail_points = [[] for _ in range(num_electrons)]

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

dt = 0.02
while True:
    alphas += np.pi * 2.0 * dt
    betas += np.pi * dt
    
    x = radius * np.cos(alphas) * np.cos(betas)
    y = radius * np.sin(alphas) * np.cos(betas)
    z = radius * np.sin(betas)
    
    electrons_scatter._offsets3d = (x, y, z)
    
    for i in range(num_electrons):
        trail_points[i].append((x[i], y[i], z[i]))
        if len(trail_points[i]) > 5:
            trail_points[i].pop(0)
        
        trail_x, trail_y, trail_z = zip(*trail_points[i])
        trails[i].set_data(trail_x, trail_y)
        trails[i].set_3d_properties(trail_z)

    plot_placeholder.pyplot(fig)
    time.sleep(0.05)
