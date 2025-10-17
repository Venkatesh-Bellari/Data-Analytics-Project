import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np
import io
import rembg
import cv2

st.set_page_config(page_title="AI Image Analyzer", page_icon="🤖", layout="centered")
st.title("🧠 AI Image Analysis Dashboard")
st.markdown("Upload an image to analyze **Age, Gender, Emotion, and more!**")

# Upload image
uploaded_file = st.file_uploader("📸 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert to array
    img_array = np.array(image)

    # --- Background Removal ---
    if st.checkbox("🧩 Remove Background"):
        with st.spinner("Removing background..."):
            output = rembg.remove(img_array)
            st.image(output, caption="Background Removed", use_container_width=True)

    # --- Face Analysis ---
    if st.checkbox("🧍 Analyze Face Attributes"):
        with st.spinner("Analyzing faces... please wait ⏳"):
            try:
                results = DeepFace.analyze(img_path=np.array(image),
                                           actions=['age', 'gender', 'emotion'],
                                           enforce_detection=False)

                # DeepFace may return a list or dict depending on image
                if isinstance(results, list):
                    results_list = results
                else:
                    results_list = [results]

                st.subheader("🧬 Analysis Results")
                for i, result in enumerate(results_list, start=1):
                    st.markdown(f"### 👤 Face {i}")
                    st.write(f"**Age:** {int(result['age'])}")
                    st.write(f"**Gender:** {result['dominant_gender'].capitalize()}")
                    st.write(f"**Emotion:** {result['dominant_emotion'].capitalize()}")

                    # Draw bounding box around face
                    region = result.get("region")
                    if region and region["w"] > 0:
                        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
                        img_copy = img_array.copy()
                        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        st.image(img_copy, caption=f"Detected Face {i}", use_container_width=True)

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
else:
    st.info("👆 Please upload an image to start analysis.")
