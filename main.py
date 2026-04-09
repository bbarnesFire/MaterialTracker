import streamlit as st
from camera_input_live import camera_input_live
from pyzbar.pyzbar import decode
from PIL import Image
import io

# Page Setup
st.set_page_config(page_title="Pro Plumbing Scanner", layout="centered")
st.title("🚰 Live Job Tracker")

# Initialize Session State for the scanned item
if "active_scan" not in st.session_state:
    st.session_state.active_scan = None

st.subheader("1. Point at Barcode")
st.caption("Using Rear Camera (Environment Mode)")

# THE LIVE SCANNER
# facing_mode="environment" forces the back camera
image_data = camera_input_live(facing_mode="environment")

if image_data:
    # Convert bytes to an image pyzbar can read
    img = Image.open(io.BytesIO(image_data.read()))
    binary_data = decode(img)

    if binary_data:
        # Get the text from the first barcode found
        scanned_text = binary_data[0].data.decode('utf-8')
        
        # Update session state and give haptic-like feedback
        if st.session_state.active_scan != scanned_text:
            st.session_state.active_scan = scanned_text
            st.toast(f"Found: {scanned_text}", icon="✅")

# THE LOGGING FORM
if st.session_state.active_scan:
    st.divider()
    st.info(f"**Current Part:** {st.session_state.active_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job_selection = st.selectbox("Assign to Job", ["Job #101", "Job #102", "Warehouse", "Van Stock"])
        qty = st.number_input("Quantity", min_value=1, value=1)
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("🔥 Log to Job")
        with col2:
            clear = st.form_submit_button("❌ Clear/Reset")

        if submit:
            # Placeholder for your Google Sheets / Database logic
            st.success(f"Logged {qty}x {st.session_state.active_scan} to {job_selection}")
            st.session_state.active_scan = None
            st.balloons()
            
        if clear:
            st.session_state.active_scan = None
            st.rerun()
else:
    st.warning("Scanning... please center the barcode in the frame.")

# Instructions for the crew
with st.expander("Help & Instructions"):
    st.write("""
    1. Open this link in **Safari** on your iPad.
    2. Tap the **Share** button and select **'Add to Home Screen'**.
    3. Allow camera access when prompted.
    4. Hold the iPad about 6-10 inches away from the barcode.
    """)
