import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="centered")
st.title("Fourier Analysis App")

# ****************************************
# [UI Inputs]
# ****************************************
st.sidebar.header("Parameters")
f_str = st.sidebar.text_input("f(t)", "sin(pi*t/10)")
delta = st.sidebar.number_input("delta", 0.01, 1.0, 0.1, 0.01)
N = st.sidebar.number_input("N (Number of samples)", 10, 1000, 200, 10)
num_coeffs = st.sidebar.number_input("Number of coefficients", 1, 100, 10, 1)

# ****************************************
# [Analyze Class]
# ****************************************
class Analyze:
    def __init__(self, f_str, N, delta):
        self.t = np.arange(N) * delta
        self.N = N
        
        # Safe evaluation context
        safe_dict = {
            "t": self.t,
            "np": np,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "pi": np.pi,
            "exp": np.exp,
            "sqrt": np.sqrt,
        }
        try:
            # Replace pi for numpy compatibility and evaluate
            f_str_np = f_str.replace("pi", "np.pi")
            self.y = eval(f_str_np, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            st.error(f"Error parsing function string: '{f_str}'. Please check the syntax. Allowed variables: 't'. Allowed functions: sin, cos, tan, exp, sqrt, pi.")
            st.stop()

    def get_cosine_coefficient(self, k):
        if k == 0:
            return np.sum(self.y) / self.N
        return (2.0 / self.N) * np.sum(self.y * np.cos(2 * np.pi * k * np.arange(self.N) / self.N))

    def get_sine_coefficient(self, k):
        return (2.0 / self.N) * np.sum(self.y * np.sin(2 * np.pi * k * np.arange(self.N) / self.N))

# ****************************************
# [Calculation]
# ****************************************
analyzer = Analyze(f_str, int(N), delta)
f0 = 1.0 / (N * delta)

frequencies = []
cos_coeffs = []
sin_coeffs = []

for i in range(int(num_coeffs) + 1):
    freq = i * f0
    cos_c = analyzer.get_cosine_coefficient(i)
    sin_c = analyzer.get_sine_coefficient(i)
    
    frequencies.append(freq)
    cos_coeffs.append(cos_c)
    sin_coeffs.append(sin_c)

df = pd.DataFrame({
    "Frequency": frequencies,
    "Cosine Coefficient": cos_coeffs,
    "Sine Coefficient": sin_coeffs
})

# ****************************************
# [Plotting]
# ****************************************
st.subheader("Fourier Coefficients")
fig, ax = plt.subplots()

# Use stem plots to mimic the 'POST' marker from OSP
markerline_cos, stemlines_cos, baseline_cos = ax.stem(
    df["Frequency"], df["Cosine Coefficient"], linefmt='r-', markerfmt='ro', basefmt='r-', label="cos"
)
plt.setp(stemlines_cos, 'color', 'r', 'linewidth', 2, 'alpha', 0.7)
plt.setp(markerline_cos, 'color', 'r', 'alpha', 0.7)

markerline_sin, stemlines_sin, baseline_sin = ax.stem(
    df["Frequency"], df["Sine Coefficient"], linefmt='b-', markerfmt='bo', basefmt='b-', label="sin"
)
plt.setp(stemlines_sin, 'color', 'b', 'linewidth', 2, 'alpha', 0.7)
plt.setp(markerline_sin, 'color', 'b', 'alpha', 0.7)

ax.set_xlabel("Frequency")
ax.set_ylabel("Coefficients")
ax.set_title("Fourier Analysis")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ****************************************
# [Data Table]
# ****************************************
st.subheader("Data Table")
st.dataframe(df.style.format("{:.4f}"))
