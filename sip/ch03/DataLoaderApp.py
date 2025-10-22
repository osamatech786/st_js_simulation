import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Loader", layout="wide")
st.title("📄 Data Loader")
st.write("This app reads data from `falling.txt` and displays it.")

# ****************************************
# Data Loading Function
# ****************************************
def load_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    t_values = []
    y_values = []
    
    for line in lines:
        if line.strip().startswith("//"):
            continue
        parts = line.strip().split()
        if len(parts) == 2:
            t_values.append(float(parts[0]))
            y_values.append(float(parts[1]))
            
    return pd.DataFrame({'Time (s)': t_values, 'Position (m)': y_values})

# ****************************************
# Loading Data
# ****************************************
data = load_data('sip/ch03/falling.txt')

# ****************************************
# Displaying Data
# ****************************************
st.subheader("Data from `falling.txt`")
st.dataframe(data)

st.subheader("Position vs. Time")
fig, ax = plt.subplots()
ax.plot(data['Time (s)'], data['Position (m)'], marker='o', linestyle='-')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Position (m)')
st.pyplot(fig)
