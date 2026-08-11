import numpy as np
import streamlit as st
from PIL import Image
from api import ApiClient

SERVER_URL = "https://adamantix-ensemble-model-mental-illness-classification.hf.space"

class SegmentationApp:
    def __init__(self, base_url):
        self.client = ApiClient(base_url)

    @staticmethod
    def overlay(image, mask):
        # convert image to RGB
        out = np.array(image.convert("RGB"))

        # create a boolean mask where the mask (halve the pixel + push the red pixel one up)
        out[mask] = out[mask] // 2 + np.array([127, 0, 0], np.uint8)
        return out

    def run(self):
        st.title("Floating Plastic Debris Image Segmentation")

        upload = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if upload is None:
            return

        image = Image.open(upload)

        if st.button("Segment"):
            with st.spinner("Waking server, first call can take ~1 min..."):
                st.session_state.result = self.client.predict(upload.getvalue())

        if "result" in st.session_state:
            return

        result = st.session_state.result
        mask = result["probs"] > 0.8 # 0.8 is a threshold based on the training notebook

        left, right = st.columns(2)
        left.image(image, caption="Original Image", use_column_width=True)
        right.image(self.overlay(image, mask), caption=f"Plastic (>{0.8:.2f})")
        st.metric("Plastic coverage", f"{100 * mask.mean():.2f}%")
        st.caption(f"Inference {result['inference_ms']} ms")

if __name__ == "__main__":
    SegmentationApp(SERVER_URL).run()