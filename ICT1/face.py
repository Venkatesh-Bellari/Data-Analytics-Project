import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np
import cv2
import io
import rembg

# -------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------
st.set_page_config(page_title="AI Smart Image Analyzer", page_icon="🤖", layout="centered")
st.title("🧠 AI Smart Image Analyzer")
st.markdown("Upload an image to analyze **Age, Gender, Emotion, detect faces, and remove background**.")

# -------------------------------------------------------
# Upload Image
# -------------------------------------------------------
uploaded_file = st.file_uploader("📸 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert to numpy array
    img_array = np.array(image)

    # ---------------------------------------------------
    # Background Removal
    # ---------------------------------------------------
    if st.checkbox("🎨 Remove Background"):
        with st.spinner("Removing background..."):
            output = rembg.remove(img_array)
            st.image(output, caption="Background Removed", use_column_width=True)

            # Download option
            buf = io.BytesIO()
            Image.fromarray(output).save(buf, format="PNG")
            st.download_button(
                label="⬇️ Download Image",
                data=buf.getvalue(),
                file_name="bg_removed.png",
                mime="image/png"
            )

    # ---------------------------------------------------
    # Face Analysis (Age, Gender, Emotion)
    # ---------------------------------------------------
    if st.checkbox("👤 Analyze Faces (Age, Gender, Emotion)"):
        with st.spinner("Analyzing faces... ⏳"):
            try:
                results = DeepFace.analyze(
                    img_path=img_array,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False,
                    detector_backend='opencv'  # Lightweight CPU detector
                )

                # DeepFace may return a list or dict
                if isinstance(results, list):
                    faces = results
                else:
                    faces = [results]

                st.subheader("🧬 Analysis Results")
                for i, face in enumerate(faces, start=1):
                    st.markdown(f"### 👤 Face {i}")
                    st.write(f"**Age:** {int(face['age'])}")
                    st.write(f"**Gender:** {face['dominant_gender'].capitalize()}")
                    st.write(f"**Emotion:** {face['dominant_emotion'].capitalize()}")

                    # Draw rectangle around face
                    region = face.get("region")
                    if region and region["w"] > 0:
                        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
                        img_copy = img_array.copy()
                        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        st.image(img_copy, caption=f"Detected Face {i}", use_container_width=True)

            except Exception as e:
                st.error("⚠️ Face analysis is not available on this platform or image contains no faces.")
                st.error(f"Error details: {str(e)}")

else:
    st.info("👆 Please upload an image to start analysis.")
