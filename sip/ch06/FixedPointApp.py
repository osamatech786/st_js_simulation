import streamlit as st
import numpy as np

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="Fixed Point Finder", layout="wide")
st.title("Fixed Point Finder for the Logistic Map")
st.write("This app computes fixed points of the logistic map using the bisection root finding method.")

# ****************************************
# Parameters
# ****************************************
st.sidebar.header("Parameters")
r = st.sidebar.number_input("r", value=0.8)
period = st.sidebar.number_input("period", value=2, step=1)
epsilon = st.sidebar.number_input("epsilon", value=0.0000001, format="%.8f")
xleft = st.sidebar.number_input("xleft", value=0.01)
xright = st.sidebar.number_input("xright", value=0.99)

# ****************************************
# Core Functions
# ****************************************
def logistic_iteration(x, r, iterations):
    y = x
    for _ in range(iterations):
        y = 4 * r * y * (1 - y)
    return y - x

def bisection(f, a, b, tol):
    if np.sign(f(a)) == np.sign(f(b)):
        return None
    while (b - a) / 2.0 > tol:
        midpoint = (a + b) / 2.0
        if np.sign(f(midpoint)) == np.sign(f(a)):
            a = midpoint
        else:
            b = midpoint
    return (a + b) / 2.0

# ****************************************
# Main Logic
# ****************************************
if st.sidebar.button("Find Fixed Point"):
    f = lambda x: logistic_iteration(x, r, period)
    x_fixed = bisection(f, xleft, xright, epsilon)

    if x_fixed is None:
        st.write("Range does not enclose a root.")
    else:
        st.subheader(f"Fixed point for period {period}: {x_fixed:.8f}")
        
        st.subheader("Trajectory")
        x = x_fixed
        trajectory = [x]
        for _ in range(2 * period + 1):
            x = 4 * r * x * (1 - x)
            trajectory.append(x)
        
        st.dataframe({'Step': range(len(trajectory)), 'x': trajectory})
