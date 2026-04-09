import streamlit as st
from barcode_reader import streamlit_barcode_reader
import pandas as pd
from datetime import datetime

# Page styling for iPad
st.set_page_config(page_title="Plumbing Job Tracker", layout="centered")

st.title("🚰 Job Site Barcode Scanner")

# 1. Job Selection
job_list = ["Job #102 - Smith", "Job #105 - Jones", "Warehouse Return", "New Job..."]
selected_job = st.selectbox("Select Target Job:", job_list)

st.divider()

# 2. The Scanner Logic
st.subheader("Scan Part Barcode")
# This opens the camera on the iPad
barcode_data = streamlit_barcode_reader(key='barcode_reader')

# 3. Handle the Scanned Data
if barcode_data:
    # Display what was scanned
    st.success(f"Scanned: {barcode_data}")
    
    # Optional: Quantity adjustment
    qty = st.number_input("Quantity", min_value=1, value=1)
    
    if st.button("Confirm Log to Job"):
        # Create a new record
        log_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Job": selected_job,
            "Part": barcode_data,
            "Quantity": qty
        }
        
        # LOGGING LOGIC:
        # If using Google Sheets, you'd use your 'Secrets' here to connect
        # For now, we'll just show the data:
        st.info(f"Logging {qty} units of {barcode_data} to {selected_job}")
        
        # Clear the scan so you can do the next one
        st.balloons()
else:
    st.info("Waiting for barcode... Point iPad camera at the label.")

# 4. View Recent Scans (Optional)
with st.expander("View Recent Activity"):
    st.write("This is where your Google Sheet data would appear.")
