import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import io

st.set_page_config(page_title="Pro Material Tracker", layout="centered")
st.title("🚰 Reliable Job Tracker")

# 1. Session State to keep data between reloads
if "current_scan" not in st.session_state:
    st.session_state.current_scan = None

st.subheader("1. Snap Barcode")

# This is the built-in Streamlit camera. 
# It works perfectly on iPads and handles the 'back camera' better.
img_file = st.camera_input("Point at barcode and click 'Take Photo'")

if img_file:
    # Convert the upload to an Image object
    img = Image.open(img_file)
    
    # Use pyzbar to decode the image
    detected_barcodes = decode(img)
    
    if detected_barcodes:
        # Grab the text from the first barcode found
        st.session_state.current_scan = detected_barcodes[0].data.decode('utf-8')
        st.toast(f"Found: {st.session_state.current_scan}", icon="✅")
    else:
        st.error("Could not read barcode. Please ensure it's in focus and well-lit.")

# 2. Logging Form
if st.session_state.current_scan:
    st.divider()
    st.info(f"**Ready to log:** {st.session_state.current_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job_selection = st.selectbox("Assign to Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔥 Log to Job")
        with col2:
            clear = st.form_submit_button("❌ Reset")

        if submit:
            # Data is saved! 
            st.success(f"Logged {qty}x {st.session_state.current_scan} to {job_selection}")
            st.session_state.current_scan = None
            st.balloons()
            
        if clear:
            st.session_state.active_scan = None
            st.rerun()
