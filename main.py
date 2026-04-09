import streamlit as st
from camera_input_live import camera_input_live
from pyzbar.pyzbar import decode
from PIL import Image
import io

# Page Setup
st.set_page_config(page_title="Pro Plumbing Scanner", layout="centered")
st.title("🚰 Live Job Tracker")

# Initialize Session State
if "active_scan" not in st.session_state:
    st.session_state.active_scan = None

st.subheader("1. Scan Barcode")

# THE FIX: Removed 'facing_mode' to stop the crash.
# Added show_controls=True so you can manually toggle to the back camera if it starts on the front.
image_data = camera_input_live(show_controls=True, key="live_scanner")

if image_data:
    # Process the image
    img = Image.open(io.BytesIO(image_data.read()))
    binary_data = decode(img)

    if binary_data:
        scanned_text = binary_data[0].data.decode('utf-8')
        
        if st.session_state.active_scan != scanned_text:
            st.session_state.active_scan = scanned_text
            st.toast(f"Found: {scanned_text}", icon="✅")

# THE LOGGING FORM
if st.session_state.active_scan:
    st.divider()
    st.info(f"**Current Part:** {st.session_state.active_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job_selection = st.selectbox("Assign to Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔥 Log to Job")
        with col2:
            clear = st.form_submit_button("❌ Reset")

        if submit:
            st.success(f"Logged {qty}x {st.session_state.active_scan} to {job_selection}")
            st.session_state.active_scan = None
            st.balloons()
            
        if clear:
            st.session_state.active_scan = None
            st.rerun()
else:
    st.warning("Center the barcode in the camera view.")
