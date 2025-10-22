import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    Computes and displays the Fraunhofer diffraction pattern using the FFT algorithm.
    """
    # ****************************************
    # Constants and Parameters
    # ****************************************
    N = 512  # Number of points
    a = 10.0  # Aperture screen dimension
    slit_width = 0.4  # Width of the slit
    LOG10 = np.log(10)
    ALPHA = np.log(1.0e-3) / LOG10  # Cutoff value for log scale

    # ****************************************
    # Create Aperture Function
    # ****************************************
    # Create a complex array to hold the aperture data
    aperture_data = np.zeros(N, dtype=complex)
    
    # Define the spatial coordinates
    x = np.linspace(-a, a, N, endpoint=False)
    
    # Define the single slit aperture: 1 inside the slit, 0 outside
    aperture_data[np.abs(x) < slit_width] = 1.0

    # ****************************************
    # Perform FFT
    # ****************************************
    # Compute the Fast Fourier Transform
    fft_result = np.fft.fft(aperture_data)
    
    # Shift the zero-frequency component to the center of the spectrum
    fft_shifted = np.fft.fftshift(fft_result)

    # ****************************************
    # Calculate Intensity
    # ****************************************
    # Intensity is the square of the magnitude of the complex FFT result
    intensity = np.abs(fft_shifted)**2
    max_intensity = np.max(intensity)
    
    # Avoid division by zero if max_intensity is zero
    if max_intensity == 0:
        max_intensity = 1.0

    # ****************************************
    # Plot Intensity Profile
    # ****************************************
    fig1, ax1 = plt.subplots()
    ax1.plot(intensity)
    ax1.set_title("Fraunhofer Diffraction Intensity")
    ax1.set_xlabel("Position")
    ax1.set_ylabel("Intensity")
    ax1.grid(True)

    # ****************************************
    # Create and Plot Raster Image (Log Scale)
    # ****************************************
    # Normalize intensity and compute log scale
    normalized_intensity = intensity / max_intensity
    # Add a small epsilon to avoid log(0)
    log_intensity = np.log10(normalized_intensity + 1e-9)

    # Apply cutoff and scale for visualization
    # This replicates the logic from the original Java code
    visual_intensity = np.zeros(N)
    mask = log_intensity > ALPHA
    visual_intensity[mask] = 254 * (1 - (log_intensity[mask] / ALPHA))
    
    # Create a 2D array for the raster image by repeating the intensity profile
    image_data = np.tile(visual_intensity, (int(N * 0.1), 1))

    fig2, ax2 = plt.subplots()
    ax2.imshow(image_data, cmap='gray', aspect='auto')
    ax2.set_title("Fraunhofer Diffraction (Log Scale Image)")
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)

    plt.show()

if __name__ == "__main__":
    main()
