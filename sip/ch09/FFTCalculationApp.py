import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("FFT Calculation with Variable Domain")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
mode = st.sidebar.number_input("Mode (harmonic)", -10, 10, 1, 1)
N = st.sidebar.select_slider("N (Number of points)", options=[16, 32, 64, 128, 256], value=32)
xmin = st.sidebar.number_input("x min", -10.0, 10.0, 0.0, 0.1)
xmax_str = st.sidebar.text_input("x max", "2*pi")

# Safely evaluate xmax_str
try:
    # Allow numpy functions in the eval context
    safe_dict = {"pi": np.pi, "np": np}
    xmax = eval(xmax_str, {"__builtins__": {}}, safe_dict)
except Exception as e:
    st.sidebar.error(f"Invalid expression for x max: {e}")
    st.stop()

# ****************************************
# [Signal Generation]
# ****************************************
x = np.linspace(xmin, xmax, N, endpoint=False)
# Generate the complex signal z = e^(i*mode*x)
z = np.exp(1j * mode * x)

# ****************************************
# [FFT Calculation]
# ****************************************
# Perform the 1D FFT
fft_z = np.fft.fft(z)
# Calculate the frequencies
delta_x = (xmax - xmin) / N
frequencies = np.fft.fftfreq(N, d=delta_x)

# Shift the FFT result and frequencies for plotting
fft_z_shifted = np.fft.fftshift(fft_z)
frequencies_shifted = np.fft.fftshift(frequencies)

# ****************************************
# [Display Results]
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Input Signal: e^(i*{mode}x)")
    
    # Plot input signal
    fig1, ax1 = plt.subplots()
    ax1.plot(x, np.real(z), '.-', label='Real Part')
    ax1.plot(x, np.imag(z), '.-', label='Imaginary Part')
    ax1.set_xlabel("x")
    ax1.set_ylabel("Value")
    ax1.set_title("Input Signal")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Display input data table
    st.write("Input Data")
    input_df = pd.DataFrame({'x': x, 'Real': np.real(z), 'Imaginary': np.imag(z)})
    st.dataframe(input_df.style.format("{:.4f}"))

with col2:
    st.subheader("FFT Result")

    # Plot FFT magnitude
    fig2, ax2 = plt.subplots()
    markerline, stemlines, baseline = ax2.stem(frequencies_shifted, np.abs(fft_z_shifted), basefmt=" ")
    plt.setp(stemlines, 'linewidth', 2)
    ax2.set_xlabel("Frequency")
    ax2.set_ylabel("Magnitude")
    ax2.set_title("Magnitude of FFT")
    ax2.grid(True)
    st.pyplot(fig2)

    # Display FFT data table
    st.write("FFT Output Data")
    output_df = pd.DataFrame({
        'Frequency': frequencies_shifted,
        'Real': np.real(fft_z_shifted),
        'Imaginary': np.imag(fft_z_shifted)
    })
    st.dataframe(output_df.style.format("{:.4f}"))
