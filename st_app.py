import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Freier Fall – Euler-Simulation", layout="wide")
st.title("🪂 Freier Fall simulieren (Euler-Verfahren)")
st.write("Dieses Tool simuliert den freien Fall (Euler) und vergleicht mit der analytischen Lösung.")

st.sidebar.header("Parameter")
y0 = st.sidebar.number_input("y₀ [m]", value=10.0, step=0.5)
v0 = st.sidebar.number_input("v₀ [m/s]", value=0.0, step=0.5)
g  = st.sidebar.number_input("g [m/s²]", value=9.8, step=0.1, min_value=0.0)
dt = st.sidebar.number_input("Δt [s]", value=0.1, step=0.01, min_value=1e-6, format="%.4f")
n  = st.sidebar.number_input("Schritte n", value=100, step=10, min_value=1)

def simulate(y0, v0, g, dt, n):
    t = np.zeros(n+1); y = np.zeros(n+1); v = np.zeros(n+1)
    t[0], y[0], v[0] = 0.0, y0, v0
    for k in range(n):
        y[k+1] = y[k] + v[k]*dt
        v[k+1] = v[k] - g*dt
        t[k+1] = t[k] + dt
    return t, y, v

t, y, v = simulate(y0, v0, g, dt, int(n))
tt = np.linspace(0, t[-1], 500)
yy = y0 + v0*tt - 0.5*g*tt**2
vv = v0 - g*tt

col1, col2 = st.columns(2)
with col1:
    st.subheader("y(t)")
    fig, ax = plt.subplots()
    ax.plot(t, y, marker='o', linestyle='-', label='Euler')
    ax.plot(tt, yy, linestyle='--', label='Analytisch')
    ax.set_xlabel('t [s]'); ax.set_ylabel('y [m]'); ax.legend()
    st.pyplot(fig, clear_figure=True)
with col2:
    st.subheader("v(t)")
    fig2, ax2 = plt.subplots()
    ax2.plot(t, v, marker='o', linestyle='-', label='Euler')
    ax2.plot(tt, vv, linestyle='--', label='Analytisch')
    ax2.set_xlabel('t [s]'); ax2.set_ylabel('v [m/s]'); ax2.legend()
    st.pyplot(fig2, clear_figure=True)

st.dataframe({'t [s]': t, 'y [m]': y, 'v [m/s]': v})