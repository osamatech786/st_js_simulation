import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("2D Fresnel Diffraction")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Simulation Parameters")
N = st.sidebar.select_slider("Grid size (N x N)", options=[128, 256, 512], value=256)
z = st.sidebar.slider("Distance to screen (z)", 1.0e5, 1.0e6, 0.5e6, 1.0e4)
radius = st.sidebar.slider("Aperture Radius", 500.0, 5000.0, 2000.0, 100.0)

# ****************************************
# [Aperture Generation]
# ****************************************
a = 6000.0  # Aperture mask dimension
x = np.linspace(-a, a, N)
y = np.linspace(-a, a, N)
xx, yy = np.meshgrid(x, y)

aperture = np.zeros((N, N), dtype=complex)
r2 = xx**2 + yy**2
aperture[r2 < radius**2] = 1

# ****************************************
# [FFT and Propagation]
# ****************************************
# Step 1: FFT of the aperture
fft_aperture = np.fft.fft2(aperture)

# Step 2: Create the propagator in the frequency domain
kx = np.fft.fftfreq(N, d=2*a/N) * 2 * np.pi
ky = np.fft.fftfreq(N, d=2*a/N) * 2 * np.pi
kx_grid, ky_grid = np.meshgrid(kx, ky)

# Wavenumber squared
k_squared = kx_grid**2 + ky_grid**2
# Wavenumber of light (assuming lambda = 1 for simplicity, so k_light = 2*pi)
k_light_squared = (2 * np.pi)**2

radical = k_light_squared - k_squared
propagator = np.zeros_like(k_squared, dtype=complex)

# Propagating waves
prop_waves = radical > 0
propagator[prop_waves] = np.exp(1j * z * np.sqrt(radical[prop_waves]))

# Evanescent waves
evan_waves = radical <= 0
propagator[evan_waves] = np.exp(-z * np.sqrt(-radical[evan_waves]))

# Step 3: Multiply FFT of aperture by propagator
fft_propagated = fft_aperture * propagator

# Step 4: Inverse FFT to get the field at the screen
field_at_screen = np.fft.ifft2(fft_propagated)

# ****************************************
# [Intensity Calculation]
# ****************************************
intensity = np.abs(field_at_screen)**2
max_intensity = np.max(intensity)
if max_intensity > 0:
    intensity_normalized = intensity / max_intensity
else:
    intensity_normalized = np.zeros_like(intensity)

# ****************************************
# [Plotting]
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader("Aperture")
    fig1, ax1 = plt.subplots()
    ax1.imshow(np.real(aperture), extent=(-a, a, -a, a), cmap='gray')
    ax1.set_title("Circular Aperture")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    st.pyplot(fig1)

with col2:
    st.subheader("Fresnel Diffraction Pattern")
    fig2, ax2 = plt.subplots()
    im = ax2.imshow(intensity_normalized, extent=(-a, a, -a, a), cmap='hot')
    ax2.set_title(f"Intensity at z = {z:.2e}")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    fig2.colorbar(im, ax=ax2)
    st.pyplot(fig2)
