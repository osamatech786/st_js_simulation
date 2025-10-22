import streamlit as st
import os

# ****************************************
# Page Configuration and Title
# ****************************************
st.set_page_config(page_title="File Extractor", layout="wide")
st.title("File Extractor")
st.write("This app reads a file, looks for specific comment markers, and extracts the content between them into new files.")

# ****************************************
# File Uploader
# ****************************************
uploaded_file = st.file_uploader("Choose a file")

# ****************************************
# File Extraction Logic
# ****************************************
if uploaded_file is not None:
    string_data = uploaded_file.getvalue().decode("utf-8")
    lines = string_data.split('\n')
    
    extracted_files = {}
    in_break = False
    current_file_content = []
    current_file_name = ""

    for line in lines:
        if line.strip() == "// start break":
            in_break = True
            current_file_content = []
        elif line.strip() == "// end break":
            in_break = False
            if current_file_name:
                extracted_files[current_file_name] = "\n".join(current_file_content)
        elif in_break:
            if not current_file_name:
                current_file_name = line.strip()[3:] + ".java"
            else:
                current_file_content.append(line)

    if extracted_files:
        st.subheader("Extracted Files")
        for file_name, content in extracted_files.items():
            st.download_button(
                label=f"Download {file_name}",
                data=content,
                file_name=file_name,
                mime="text/plain"
            )
