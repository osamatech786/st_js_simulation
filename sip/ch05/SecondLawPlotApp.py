import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Kepler's Second Law", layout="wide")
st.title("Kepler's Second Law")
st.write("This app demonstrates Kepler's second law by plotting the log of the planet's semi-major axis vs. the log of the orbital period.")

# ****************************************
# Planetary Data
# ****************************************
period = np.array([0.241, 0.615, 1.0, 1.88, 11.86, 29.50, 84.0, 165, 248])
a = np.array([0.387, 0.723, 1.0, 1.523, 5.202, 9.539, 19.18, 30.06, 39.44])

data = pd.DataFrame({'T (years)': period, 'a (AU)': a})

# ****************************************
# Data Display and Plotting
# ****************************************
st.subheader("Planetary Data")
st.dataframe(data)

st.subheader("Log-Log Plot")
fig, ax = plt.subplots()
ax.loglog(a, period, 'o')
ax.set_xlabel("ln(a)")
ax.set_ylabel("ln(T)")
ax.grid(True, which="both", ls="-")
st.pyplot(fig)
