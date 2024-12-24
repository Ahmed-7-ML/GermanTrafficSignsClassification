import streamlit as st
import pickle
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from ImageManipulations import ImageManipulations  # استيراد الكلاس الخاص بالتحسين

# تحميل نموذج KNN المحفوظ
with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)

# تحويل الصورة إلى مصفوفة NumPy لجعلها جاهزة للتنبؤ


def preprocess_image(image):
    image_resized = cv2.resize(image, (32, 32))
    image_array = np.array(image_resized, dtype=np.float32) / 255.0
    return image_array.reshape(1, -1)


# واجهة المستخدم Streamlit
st.title("تصنيف الصور أو تحسينها")

# رفع الصورة من المستخدم
uploaded_image = st.file_uploader(
    "اختار صورة لتحسينها أو التنبؤ بها", type=["jpg", "png", "jpeg"])

# اختيارات للمستخدم
options = ["تنبؤ بالصورة (Prediction)", "تحسين الصورة (Enhancement)"]
selected_option = st.selectbox("اختار الإجراء المطلوب", options)

# إذا كانت الصورة محملة
if uploaded_image is not None:
    # تحويل الصورة إلى مصفوفة NumPy
    image = Image.open(uploaded_image)
    image = np.array(image)

    # عرض الصورة المدخلة
    st.image(image, caption="الصورة المدخلة", use_column_width=True)

    # إذا اختار المستخدم التنبؤ بالصورة
    if selected_option == "تنبؤ بالصورة (Prediction)":
        processed_image = preprocess_image(image)
        prediction = knn_model.predict(processed_image)
        st.write(f"التصنيف: {prediction[0]}")

    # إذا اختار المستخدم تحسين الصورة
    elif selected_option == "تحسين الصورة (Enhancement)":
        # تحويل الصورة إلى كائن ImageEnhancements
        enhancer = ImageManipulations(uploaded_image)

        # تطبيق بعض العمليات (تقدر تضيف أكتر بناءً على احتياجك)
        enhancer.histogram_equalization()

        # عرض الصورة المحسّنة
        st.image(enhancer.manipulated, caption="الصورة المحسّنة",
                use_column_width=True)

        # حفظ الصورة المحسّنة
        enhancer.save('enhanced_image.jpg')
        st.download_button("تحميل الصورة المحسّنة", "enhanced_image.jpg")
