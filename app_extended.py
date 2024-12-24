import streamlit as st
import pickle
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from ImageManipulations import ImageManipulations

with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

def preprocess_image(image):
    image_resized = cv2.resize(image, (32, 32))
    image_array = np.array(image_resized, dtype=np.float32) / 255.0
    return image_array.reshape(1, -1)

st.title("تصنيف الصور أو تحسينها")

uploaded_image = st.file_uploader(
    "اختار صورة لتحسينها أو التنبؤ بها", type=["jpg", "png", "jpeg"])

options = ["تنبؤ بالصورة (Prediction)", "تحسين الصورة (Enhancement)"]
selected_option = st.selectbox("اختار الإجراء المطلوب", options)

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    image = np.array(image)

    st.image(image, caption="الصورة المدخلة", use_column_width=True)

    if selected_option == "تنبؤ بالصورة (Prediction)":
        processed_image = preprocess_image(image)
        prediction = knn_model.predict(processed_image)
        st.write(f"التصنيف: {prediction[0]}")

    elif selected_option == "تحسين الصورة (Enhancement)":
        enhancer = ImageManipulations(uploaded_image)

        enhancer.histogram_equalization()

        st.image(enhancer.manipulated, caption="الصورة المحسّنة",
                use_column_width=True)

        enhancer.save('enhanced_image.jpg')
        st.download_button("تحميل الصورة المحسّنة", "enhanced_image.jpg")
