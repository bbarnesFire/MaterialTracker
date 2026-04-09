import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
from pyzbar.pyzbar import decode
import queue  # <--- Added this to bridge the threads

st.set_page_config(page_title="Pro Material Scanner", layout="centered")

st.title("🚰 Rear-Cam Job Tracker")

# This queue will hold the barcodes found by the camera thread
if "result_queue" not in st.session_state:
    st.session_state.result_queue = queue.Queue()

class BarcodeProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        barcodes = decode(img)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            
            # Draw on the video feed
            x, y, w, h = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Push the result to the queue to be read by the main UI
            st.session_state.result_queue.put(barcode_data)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Camera stream with the proper rear-cam constraints
webrtc_ctx = webrtc_streamer(
    key="barcode-scanner",
    video_processor_factory=BarcodeProcessor,
    media_stream_constraints={
        "video": {
            "facingMode": "environment",
            "width": {"ideal": 1280},
            "height": {"ideal": 720}
        },
        "audio": False,
    },
    async_processing=True,
)

# Pull the latest scan out of the queue
if not st.session_state.result_queue.empty():
    st.session_state.active_scan = st.session_state.result_queue.get()

# Form Logic
if "active_scan" in st.session_state and st.session_state.active_scan:
    st.divider()
    st.info(f"**Scanned Part:** {st.session_state.active_scan}")
    
    with st.form("log_form", clear_on_submit=True):
        job = st.selectbox("Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Qty", min_value=1, value=1)
        
        if st.form_submit_button("Log to Job"):
            st.success(f"Logged {st.session_state.active_scan} to {job}")
            st.session_state.active_scan = None # Clear after submit
            st.balloons()
