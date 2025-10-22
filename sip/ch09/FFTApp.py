import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("1D FFT of a Complex Exponential")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
mode = st.sidebar.number_input("Mode (harmonic)", -10, 10, -1, 1)
N = st.sidebar.select_slider("N (Number of points)", options=[8, 16, 32, 64, 128], value=8)

# ****************************************
# [Signal Generation]
# ****************************************
# Generate the signal x from 0 to 2*pi
x = np.linspace(0, 2 * np.pi, N, endpoint=False)
# Generate the complex signal z = e^(i*mode*x)
z = np.exp(1j * mode * x)

# ****************************************
# [FFT Calculation]
# ****************************************
# Perform the 1D FFT
fft_z = np.fft.fft(z)

# ****************************************
# [Display Results]
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Input Signal: e^(i*{mode}x)")
    
    # Plot input signal
    fig1, ax1 = plt.subplots()
    ax1.plot(x, np.real(z), 'o-', label='Real Part')
    ax1.plot(x, np.imag(z), 'o-', label='Imaginary Part')
    ax1.set_xlabel("x")
    ax1.set_ylabel("Value")
    ax1.set_title("Input Signal")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Display input data table
    st.write("Input Data")
    input_df = pd.DataFrame({
        'x': x,
        'Real': np.real(z),
        'Imaginary': np.imag(z)
    })
    st.dataframe(input_df.style.format("{:.4f}"))

with col2:
    st.subheader("FFT Result")

    # Plot FFT magnitude
    fig2, ax2 = plt.subplots()
    k = np.arange(N)
    markerline, stemlines, baseline = ax2.stem(k, np.abs(fft_z), basefmt=" ")
    plt.setp(stemlines, 'linewidth', 2)
    ax2.set_xlabel("Frequency Index (k)")
    ax2.set_ylabel("Magnitude")
    ax2.set_title("Magnitude of FFT")
    ax2.grid(True)
    st.pyplot(fig2)

    # Display FFT data table
    st.write("FFT Output Data")
    output_df = pd.DataFrame({
        'Index (k)': k,
        'Real': np.real(fft_z),
        'Imaginary': np.imag(fft_z)
    })
    st.dataframe(output_df.style.format("{:.4f}"))
