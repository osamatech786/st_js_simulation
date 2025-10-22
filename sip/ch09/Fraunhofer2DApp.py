import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("2D Fraunhofer Diffraction")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Simulation Parameters")
n = st.sidebar.select_slider("Grid size (n x n)", options=[64, 128, 256, 512], value=256)
aperture_type = st.sidebar.selectbox("Aperture Type", ["Circular", "Rectangular", "Double Slit"])

# Aperture-specific parameters
radius = 0.0
width = 0.0
height = 0.0
slit_width = 0.0
slit_separation = 0.0
slit_height = 0.0

if aperture_type == "Circular":
    radius = st.sidebar.slider("Radius", 0.1, 2.0, 0.5, 0.1)
elif aperture_type == "Rectangular":
    width = st.sidebar.slider("Width", 0.1, 2.0, 0.5, 0.1)
    height = st.sidebar.slider("Height", 0.1, 2.0, 2.0, 0.1)
elif aperture_type == "Double Slit":
    slit_width = st.sidebar.slider("Slit Width", 0.05, 1.0, 0.1, 0.05)
    slit_separation = st.sidebar.slider("Slit Separation", 0.1, 2.0, 0.5, 0.1)
    slit_height = st.sidebar.slider("Slit Height", 0.1, 2.0, 2.0, 0.1)

# ****************************************
# [Aperture Generation]
# ****************************************
a = 10.0  # Aperture screen dimension
x = np.linspace(-a, a, n)
y = np.linspace(-a, a, n)
xx, yy = np.meshgrid(x, y)

aperture = np.zeros((n, n), dtype=complex)

if aperture_type == "Circular":
    r = np.sqrt(xx**2 + yy**2)
    aperture[r < radius] = 1
elif aperture_type == "Rectangular":
    aperture[(np.abs(xx) < width / 2) & (np.abs(yy) < height / 2)] = 1
elif aperture_type == "Double Slit":
    slit1 = (np.abs(xx - slit_separation / 2) < slit_width / 2) & (np.abs(yy) < slit_height / 2)
    slit2 = (np.abs(xx + slit_separation / 2) < slit_width / 2) & (np.abs(yy) < slit_height / 2)
    aperture[slit1 | slit2] = 1

# ****************************************
# [FFT and Intensity Calculation]
# ****************************************
# Perform 2D FFT and shift
diffraction_pattern = np.fft.fftshift(np.fft.fft2(aperture))
intensity = np.abs(diffraction_pattern)**2

# Normalize and apply log scale for better visualization
max_intensity = np.max(intensity)
if max_intensity > 0:
    intensity_log = np.log10(intensity / max_intensity + 1e-9) # Add small epsilon to avoid log(0)
else:
    intensity_log = np.zeros_like(intensity)

# ****************************************
# [Plotting]
# ****************************************
col1, col2 = st.columns(2)

with col1:
    st.subheader("Aperture")
    fig1, ax1 = plt.subplots()
    ax1.imshow(np.real(aperture), extent=(-a, a, -a, a), cmap='gray')
    ax1.set_title(f"{aperture_type} Aperture")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    st.pyplot(fig1)

with col2:
    st.subheader("Diffraction Pattern (Log Intensity)")
    fig2, ax2 = plt.subplots()
    # The spatial frequency coordinates
    k = np.fft.fftshift(np.fft.fftfreq(n, d=2*a/n))
    im = ax2.imshow(intensity_log, extent=(k[0], k[-1], k[0], k[-1]), cmap='hot', vmin=np.min(intensity_log), vmax=np.max(intensity_log))
    ax2.set_title("Fraunhofer Diffraction")
    ax2.set_xlabel("k_x")
    ax2.set_ylabel("k_y")
    fig2.colorbar(im, ax=ax2)
    st.pyplot(fig2)
