import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Job Tracker")

# 1. Input: Select the Job
job_number = st.selectbox("Select Job", ["Job #102 - Smith", "Job #105 - Jones", "Warehouse Return"])

# 2. Input: Scan Barcode (Streamlit has components for camera scanning)
barcode_input = st.text_input("Scan Barcode or Type ID")

# 3. Input: Quantity
qty = st.number_input("Quantity", min_value=1, value=1)

if st.button("Log to Job"):
    # This is where the Python magic happens
    new_entry = {
        "Timestamp": datetime.now(),
        "Job": job_number,
        "Part": barcode_input,
        "Qty": qty
    }
    # Here you would append this data to a Google Sheet or CSV
    st.success(f"Logged {qty}x {barcode_input} to {job_number}")
