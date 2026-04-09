import streamlit as st
from streamlit_zxing import zxing_barcode_scanner
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Plumbing Tracker", page_icon="🚰")

st.title("🚰 Job Site Tracker")

# 2. Initialize "Memory" (Session State)
# This keeps the scanned barcode on the screen while you fill out the rest of the form
if "current_scan" not in st.session_state:
    st.session_state.current_scan = None

# 3. The Scanner Section
st.subheader("1. Scan Barcode")
with st.container(border=True):
    # This component opens the camera
    barcode_result = zxing_barcode_scanner(key='barcode_scanner')

    if barcode_result:
        # If barcode_result is a dict, get 'barcodeValue', otherwise use as is
        scanned_val = barcode_result.get('barcodeValue') if isinstance(barcode_result, dict) else barcode_result
        if scanned_val:
            st.session_state.current_scan = scanned_val
            st.toast(f"Detected: {scanned_val}", icon="✅")

# 4. The Logging Form
st.subheader("2. Part Details")
if st.session_state.current_scan:
    st.info(f"**Current Part:** {st.session_state.current_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job_name = st.selectbox("Assign to Job:", ["Job #101 - Smith", "Job #102 - Jones", "Warehouse Stock"])
        quantity = st.number_input("Quantity", min_value=1, value=1)
        notes = st.text_input("Notes (Optional)")
        
        submit = st.form_submit_button("Log Part to Job")
        
        if submit:
            # Here is where the data is actually "saved"
            new_data = {
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Part": st.session_state.current_scan,
                "Job": job_name,
                "Qty": quantity,
                "Notes": notes
            }
            
            # For now, we'll just show the success message.
            # Next step: append to a Google Sheet!
            st.success(f"Logged {quantity}x {st.session_state.current_scan} to {job_name}")
            
            # Clear the scan memory so we can do the next one
            st.session_state.current_scan = None
            st.balloons()
else:
    st.warning("No part scanned yet. Point your camera at a barcode above.")

# 5. Dashboard (Optional view of recent activity)
with st.expander("Recent Scans"):
    st.write("Recent history will appear here once connected to a database.")
