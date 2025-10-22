import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("2D FFT Calculation App")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
x_mode = st.sidebar.number_input("x mode", -10, 10, 0, 1)
y_mode = st.sidebar.number_input("y mode", -10, 10, 1, 1)
nx = st.sidebar.select_slider("Nx (Grid points in x)", options=[8, 16, 32, 64, 128], value=16)
ny = st.sidebar.select_slider("Ny (Grid points in y)", options=[8, 16, 32, 64, 128], value=16)

# The domain is fixed from 0 to 2*pi as in the Java example's core logic
xmin, xmax = 0, 2 * np.pi
ymin, ymax = 0, 2 * np.pi

# ****************************************
# [Signal Generation]
# ****************************************
x = np.linspace(xmin, xmax, nx, endpoint=False)
y = np.linspace(ymin, ymax, ny, endpoint=False)
xx, yy = np.meshgrid(x, y)

# Generate the complex signal: z = exp(i*x_mode*x) * exp(i*y_mode*y)
z_data = np.exp(1j * x_mode * xx) * np.exp(1j * y_mode * yy)

# ****************************************
# [FFT Calculation]
# ****************************************
# Perform 2D FFT and shift the zero-frequency component to the center
fft_result = np.fft.fftshift(np.fft.fft2(z_data))
fft_magnitude = np.abs(fft_result)

# ****************************************
# [Plotting]
# ****************************************
st.subheader("Input Signal and 2D FFT Result")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Plot 1: Real part of the input signal
im1 = axes[0].imshow(np.real(z_data), extent=[xmin, xmax, ymin, ymax], origin='lower', cmap='viridis')
axes[0].set_title("Real Part of Input Signal")
axes[0].set_xlabel("x")
axes[0].set_ylabel("y")
fig.colorbar(im1, ax=axes[0])

# Plot 2: Imaginary part of the input signal
im2 = axes[1].imshow(np.imag(z_data), extent=[xmin, xmax, ymin, ymax], origin='lower', cmap='viridis')
axes[1].set_title("Imaginary Part of Input Signal")
axes[1].set_xlabel("x")
axes[1].set_ylabel("y")
fig.colorbar(im2, ax=axes[1])

# Plot 3: Magnitude of the 2D FFT
# Frequency domain extents
kx_min, kx_max = -nx / (2 * (xmax - xmin)), nx / (2 * (xmax - xmin))
ky_min, ky_max = -ny / (2 * (ymax - ymin)), ny / (2 * (ymax - ymin))
im3 = axes[2].imshow(fft_magnitude, extent=[kx_min, kx_max, ky_min, ky_max], origin='lower', cmap='hot')
axes[2].set_title("Magnitude of 2D FFT")
axes[2].set_xlabel("k_x")
axes[2].set_ylabel("k_y")
fig.colorbar(im3, ax=axes[2])

plt.tight_layout()
st.pyplot(fig)
