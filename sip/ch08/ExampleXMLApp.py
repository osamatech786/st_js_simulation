import streamlit as st
import xml.etree.ElementTree as ET
import numpy as np

st.set_page_config(page_title="XML Example", layout="wide")
st.title("XML Read/Write Example")
st.write("This app demonstrates how to write and read data to and from an XML file.")

# ****************************************
# Event Handlers
# ****************************************
if st.button("Write XML File"):
    root = ET.Element("data")
    ET.SubElement(root, "comment").text = "An XML description of an array."
    
    x_positions = ET.SubElement(root, "x_positions")
    x_positions.text = np.array2string(np.array([1, 3, 4]))
    
    x_velocities = ET.SubElement(root, "x_velocities")
    x_velocities.text = np.array2string(np.array([0, -1, 1]))
    
    tree = ET.ElementTree(root)
    tree.write("particle_configuration.xml")
    st.success("Wrote particle_configuration.xml")

if st.button("Read XML File"):
    try:
        tree = ET.parse("particle_configuration.xml")
        root = tree.getroot()
        
        comment_element = root.find("comment")
        if comment_element is not None and comment_element.text is not None:
            st.write(f"Comment: {comment_element.text}")
        
        x_pos_element = root.find("x_positions")
        x_vel_element = root.find("x_velocities")
        
        if (x_pos_element is not None and x_pos_element.text is not None and
                x_vel_element is not None and x_vel_element.text is not None):
            
            x_pos_str = x_pos_element.text
            x_pos = np.fromstring(x_pos_str.strip('[]'), sep=' ')
            
            x_vel_str = x_vel_element.text
            x_vel = np.fromstring(x_vel_str.strip('[]'), sep=' ')
            
            st.write("Data:")
            for i in range(len(x_pos)):
                st.write(f"x[{i}]={x_pos[i]}, vx[{i}]={x_vel[i]}")
        else:
            st.warning("Could not find position or velocity data in XML file.")
            
    except FileNotFoundError:
        st.error("File not found. Please write the file first.")
