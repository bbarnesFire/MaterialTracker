import streamlit as st
from PIL import Image
from pyzbar.pyzbar import decode
import pandas as pd
from datetime import datetime

# Page Setup
st.set_page_config(page_title="Plumbing Tracker", layout="centered")
st.title("🚰 Reliable Job Tracker")

# 1. Memory Setup
if "last_scan" not in st.session_state:
    st.session_state.last_scan = None

# 2. Camera Input
st.subheader("Step 1: Scan Barcode")
img_file = st.camera_input("Take a photo of the barcode")

if img_file:
    # Process the image
    img = Image.open(img_file)
    results = decode(img)
    
    if results:
        # Get the first barcode found
        st.session_state.last_scan = results[0].data.decode('utf-8')
        st.toast(f"Found: {st.session_state.last_scan}", icon="✅")
    else:
        st.warning("No barcode detected. Try to get a clearer, closer shot.")

# 3. Data Entry Form
if st.session_state.last_scan:
    st.divider()
    st.subheader("Step 2: Log Details")
    st.info(f"**Part Scanned:** {st.session_state.last_scan}")
    
    with st.form("inventory_form", clear_on_submit=True):
        job = st.selectbox("Select Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        submitted = st.form_submit_button("Submit to Logs")
        
        if submitted:
            # This is where you'd write to your Google Sheet
            st.success(f"Successfully logged {qty}x {st.session_state.last_scan} to {job}")
            
            # Reset the scan for the next item
            st.session_state.last_scan = None
            st.balloons()
