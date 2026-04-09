import streamlit as st
from camera_input_live import camera_input_live
from pyzbar.pyzbar import decode
from PIL import Image
import io

st.set_page_config(page_title="Pro Plumbing Scanner", layout="centered")

# 1. Title and Instructions
st.title("🚰 Rear-Cam Job Tracker")
st.write("If it shows the selfie cam, look for the 'Flip' icon below the feed.")

# 2. Memory for the scan
if "active_scan" not in st.session_state:
    st.session_state.active_scan = None

# 3. THE LIVE SCANNER 
# We are using 'controls=True' which is the standard for this library 
# to show the camera-flip button on iOS devices.
image_data = camera_input_live(show_controls=True, key="rear_cam_scanner")

if image_data:
    # Decode the barcode
    img = Image.open(io.BytesIO(image_data.read()))
    binary_data = decode(img)

    if binary_data:
        scanned_text = binary_data[0].data.decode('utf-8')
        if st.session_state.active_scan != scanned_text:
            st.session_state.active_scan = scanned_text
            st.toast(f"Found: {scanned_text}", icon="✅")

# 4. The Form
if st.session_state.active_scan:
    st.divider()
    st.info(f"**Part:** {st.session_state.active_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job = st.selectbox("Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Qty", min_value=1, value=1)
        
        if st.form_submit_button("Log to Job"):
            st.success(f"Logged {st.session_state.active_scan}")
            st.session_state.active_scan = None
            st.balloons()
