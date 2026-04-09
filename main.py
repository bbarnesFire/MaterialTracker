import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
from pyzbar.pyzbar import decode
import queue

st.set_page_config(page_title="Big Screen Scanner", layout="wide") # Use wide mode

# --- CUSTOM CSS FOR BIG FEED ---
st.markdown("""
    <style>
    /* Force the WebRTC container to be larger */
    div[data-testid="stWebSrtcreamer"] iframe {
        width: 100% !important;
        height: 500px !important;
    }
    /* Make the form area clean */
    .stForm {
        border: 2px solid #4CAF50;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚰 High-Vis Material Tracker")

if "result_queue" not in st.session_state:
    st.session_state.result_queue = queue.Queue()

class BarcodeProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        barcodes = decode(img)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            # Visual feedback on the feed
            x, y, w, h = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            st.session_state.result_queue.put(barcode_data)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- BIG VIDEO LAYOUT ---
col1, col2, col3 = st.columns([1, 6, 1]) # Center the 6-unit wide camera

with col2:
    webrtc_ctx = webrtc_streamer(
        key="barcode-scanner",
        video_processor_factory=BarcodeProcessor,
        # 'ideal' encourages the browser to use higher resolution
        media_stream_constraints={
            "video": {
                "facingMode": "environment",
                "width": {"ideal": 1920}, 
                "height": {"ideal": 1080}
            },
            "audio": False,
        },
        async_processing=True,
    )

# --- RESULTS AREA ---
if not st.session_state.result_queue.empty():
    st.session_state.active_scan = st.session_state.result_queue.get()

if "active_scan" in st.session_state and st.session_state.active_scan:
    st.success(f"### Current Scan: {st.session_state.active_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        st.write("Confirm details below:")
        qty = st.number_input("How many?", min_value=1, value=1)
        job = st.text_input("Job Name/Number", value="Main Project") # No selector, just a field
        
        if st.form_submit_button("Submit Entry"):
            st.success(f"Logged {qty}x {st.session_state.active_scan} to {job}")
            st.session_state.active_scan = None
            st.balloons()
