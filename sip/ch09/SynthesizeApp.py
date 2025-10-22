import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Fourier Synthesis App")

# ****************************************
# [Default Coefficients]
# ****************************************
DEFAULT_SINE_COEFFS = pd.DataFrame({'Coefficient': [1.0, 0, 1.0/3.0, 0, 1.0/5.0, 0, 1.0/7.0]})
DEFAULT_COS_COEFFS = pd.DataFrame({'Coefficient': [0.0, 0, 0, 0, 0, 0, 0]})

# ****************************************
# [Session State Initialization]
# ****************************************
if 'sin_coeffs' not in st.session_state:
    st.session_state.sin_coeffs = DEFAULT_SINE_COEFFS.copy()
if 'cos_coeffs' not in st.session_state:
    st.session_state.cos_coeffs = DEFAULT_COS_COEFFS.copy()

# ****************************************
# [Synthesis Function]
# ****************************************
def synthesize_function(x, period, cos_coeffs, sin_coeffs):
    """Synthesizes a function from its Fourier coefficients."""
    y = np.zeros_like(x)
    components = []
    
    # Add the DC component (c_0)
    if len(cos_coeffs) > 0:
        y += cos_coeffs[0]
        components.append(np.full_like(x, cos_coeffs[0]))

    # Add the AC components (n > 0)
    k = 2 * np.pi / period
    max_len = max(len(cos_coeffs), len(sin_coeffs))
    
    for n in range(1, max_len):
        cos_term = 0
        sin_term = 0
        if n < len(cos_coeffs):
            cos_term = cos_coeffs[n] * np.cos(n * k * x)
        if n < len(sin_coeffs):
            sin_term = sin_coeffs[n] * np.sin(n * k * x)
        
        y += cos_term + sin_term
        components.append(cos_term + sin_term)
        
    return y, components

# ****************************************
# [UI Controls]
# ****************************************
st.sidebar.header("Parameters")
xmin = st.sidebar.number_input("x min", -5.0, 5.0, -1.0, 0.1)
xmax = st.sidebar.number_input("x max", -5.0, 5.0, 1.0, 0.1)
N = st.sidebar.slider("Number of points (N)", 100, 1000, 300, 50)
period = st.sidebar.number_input("Period", 0.1, 10.0, 1.0, 0.1)

if st.sidebar.button("Reset Coefficients to Square Wave"):
    st.session_state.sin_coeffs = DEFAULT_SINE_COEFFS.copy()
    st.session_state.cos_coeffs = DEFAULT_COS_COEFFS.copy()

st.sidebar.subheader("Cosine Coefficients (c_n)")
st.session_state.cos_coeffs = st.sidebar.data_editor(st.session_state.cos_coeffs, num_rows="dynamic")

st.sidebar.subheader("Sine Coefficients (s_n)")
st.session_state.sin_coeffs = st.sidebar.data_editor(st.session_state.sin_coeffs, num_rows="dynamic")

# ****************************************
# [Calculation and Plotting]
# ****************************************
x_vals = np.linspace(xmin, xmax, N)
cos_c = st.session_state.cos_coeffs['Coefficient'].values
sin_c = st.session_state.sin_coeffs['Coefficient'].values

y_synthesized, y_components = synthesize_function(x_vals, period, cos_c, sin_c)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Synthesized Function")
    fig1, ax1 = plt.subplots()
    ax1.plot(x_vals, y_synthesized)
    ax1.set_xlabel("x")
    ax1.set_ylabel("f(x)")
    ax1.set_title("Fourier Synthesis")
    ax1.grid(True)
    st.pyplot(fig1)

with col2:
    st.subheader("Individual Components")
    fig2, ax2 = plt.subplots()
    for i, component in enumerate(y_components):
        ax2.plot(x_vals, component, label=f'n={i}')
    ax2.set_xlabel("x")
    ax2.set_ylabel("Component Value")
    ax2.set_title("Function Components")
    ax2.legend(loc='upper right')
    ax2.grid(True)
    st.pyplot(fig2)
