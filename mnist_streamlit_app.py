import streamlit as st
import torch
import torch.nn as nn
from PIL import Image, ImageOps
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Define the same model architecture as in the notebook
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10)
)

# Page config
st.set_page_config(page_title="MNIST Digit Classifier", page_icon="🔢", layout="wide")

# Title
st.title("🔢 MNIST Digit Classifier")
st.markdown("Draw a digit (0-9) and watch the neural network classify it in real-time!")

# Sidebar for model loading
with st.sidebar:
    st.header("Model Status")

    model_file = st.file_uploader("Upload trained model (.pth)", type=['pth'])

    if model_file is not None:
        try:
            model.load_state_dict(torch.load(model_file, map_location=torch.device('cpu')))
            model.eval()
            st.success("Model loaded successfully!")
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            model_file = None
    else:
        st.warning("Please train and upload a model first")
        st.markdown("""
        **To get a model:**
        1. Run `mnist_sequential.ipynb`
        2. Add this cell after training:
        ```python
        torch.save(model.state_dict(), 'mnist_model.pth')
        ```
        3. Download `mnist_model.pth`
        4. Upload it here
        """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Draw Here")

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgb(0, 0, 0)",  # Black background
        stroke_width=20,
        stroke_color="rgb(255, 255, 255)",  # White stroke
        background_color="rgb(0, 0, 0)",
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
    )

    if st.button("Clear Canvas", use_container_width=True):
        st.rerun()

with col2:
    st.subheader("Prediction")

    if canvas_result.image_data is not None and model_file is not None:
        # Get the image from canvas
        img = canvas_result.image_data

        # Convert to PIL Image
        img_pil = Image.fromarray(img.astype('uint8'), 'RGBA')

        # Convert to grayscale
        img_gray = img_pil.convert('L')

        # Resize to 28x28
        img_resized = img_gray.resize((28, 28), Image.Resampling.LANCZOS)

        # Invert colors (MNIST has white digits on black background)
        img_inverted = ImageOps.invert(img_resized)

        # Convert to numpy array and normalize
        img_array = np.array(img_inverted, dtype=np.float32) / 255.0

        # Convert to torch tensor
        img_tensor = torch.from_numpy(img_array).unsqueeze(0).unsqueeze(0)

        # Make prediction
        with torch.no_grad():
            output = model(img_tensor.squeeze(1))
            probabilities = torch.nn.functional.softmax(output, dim=1)
            predicted_digit = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_digit].item() * 100

        # Display prediction
        st.markdown(f"## Predicted Digit: **{predicted_digit}**")
        st.markdown(f"### Confidence: **{confidence:.1f}%**")

        # Show probability distribution
        st.markdown("#### Probability Distribution")
        prob_dict = {str(i): float(probabilities[0][i]) for i in range(10)}
        st.bar_chart(prob_dict)

        # Show processed image
        with st.expander("See processed image (28x28)"):
            st.image(img_inverted, width=140, caption="This is what the model sees")

    elif model_file is None:
        st.info("👈 Upload a trained model to start classifying")
    else:
        st.info("👈 Draw a digit on the canvas")

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. **Upload a trained model** using the sidebar
    2. **Draw a digit** (0-9) on the black canvas
    3. **Watch the prediction** update in real-time
    4. **Clear and try again** with different digits

    **Tips for better results:**
    - Draw digits centered in the canvas
    - Make digits reasonably large
    - Try to match the MNIST style (similar to handwritten digits)
    """)
