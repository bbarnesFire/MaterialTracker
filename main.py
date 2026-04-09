import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import cv2
from pyzbar.pyzbar import decode

st.set_page_config(page_title="Pro Plumbing Scanner", layout="centered")

st.title("🚰 Rear-Cam Job Tracker")
st.write("Allow camera access. This should use your rear camera automatically.")

# Session state
if "active_scan" not in st.session_state:
    st.session_state.active_scan = None


# 🎥 Video Processor for barcode scanning
class BarcodeProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        barcodes = decode(img)

        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_data = barcode.data.decode("utf-8")

            # Draw box
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Put text
            cv2.putText(
                img,
                barcode_data,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            # Save to session (only if new)
            if st.session_state.active_scan != barcode_data:
                st.session_state.active_scan = barcode_data

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# 🎥 Camera stream
webrtc_ctx = webrtc_streamer(
    key="barcode-scanner",
    video_processor_factory=BarcodeProcessor,
    media_stream_constraints={
        "video": {"facingMode": "environment"},  # 🔥 rear cam request
        "audio": False,
    },
    async_processing=True,
)

# 🔔 Show scan result
if st.session_state.active_scan:
    st.toast(f"Found: {st.session_state.active_scan}", icon="✅")

    st.divider()
    st.info(f"**Part:** {st.session_state.active_scan}")

    with st.form("log_form", clear_on_submit=True):
        job = st.selectbox("Job", ["Job #101", "Job #102", "Warehouse"])
        qty = st.number_input("Qty", min_value=1, value=1)

        if st.form_submit_button("Log to Job"):
            st.success(f"Logged {st.session_state.active_scan} to {job} (x{qty})")
            st.session_state.active_scan = None
            st.balloons()
