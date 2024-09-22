import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
import base64

# Function to convert image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Load the model
model = tf.keras.models.load_model('model/model.h5')

# Define a function to preprocess the image
def preprocess_image(image):
    image = image.convert('RGB')
    image = image.resize((224, 224))  # Adjust size according to your model
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

# Define a function to make predictions
def predict(image):
    image_array = preprocess_image(image)
    predictions = model.predict(image_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    return predicted_class

# Convert the background image to base64
background_image_path = "D:\HOPE\Projects\Chest cancer classification\End-to-End-Chest-Cancer-Classification\img1.jpg"  # Replace with your image path
background_image_base64 = get_base64_image(background_image_path)

# Custom CSS for background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Apply custom CSS directly in Streamlit
st.markdown("""
<style>
.custom-title {
    font-family: 'Quicksand', sans-serif;
    font-weight: bold;
    font-size: 36px; /* Adjust size as needed */
    text-align: center;
    color: #00000; /* Adjust color as needed */
}
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown('<h1 class="custom-title">🩺Chest Cancer Classification🎗️</h1>', unsafe_allow_html=True)


# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open and display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Predict
    with st.spinner("Classifying..."):
        result = predict(image)
    
    # Display result based on prediction
    if result == 0:
        st.markdown("<h1 style='text-align: center; color: #ff0000;'>Cancer Detected</h1>", unsafe_allow_html=True)
        st.write("It appears that the image shows signs of cancer. Please consult a healthcare professional for further analysis and treatment.")
    elif result == 1:
        st.markdown("<h1 style='text-align: center; color: #00ff00;'>Normal</h1>", unsafe_allow_html=True)
        st.write("The image appears normal. However, it's always good to follow up with regular check-ups.")
    else:
        st.markdown("<h1 style='text-align: center; color: #ffa500;'>Uncertain</h1>", unsafe_allow_html=True)
        st.write("The prediction is uncertain. Please consult a healthcare professional for a thorough diagnosis.")
