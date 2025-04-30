import streamlit as st
from PIL import Image
import io
import base64
from bedrock_helper import get_image_description
import os

# Page config
st.set_page_config(
    page_title="Image Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("Image Analyzer")
st.markdown("Upload an image and get AI-powered analysis using Claude 3.5 Sonnet")

# Sidebar with information
with st.sidebar:
    st.header("About")
    st.info(
        "This app uses Amazon Bedrock's Claude 3.5 Sonnet model to analyze "
        "images and provide detailed descriptions of their content."
    )
    st.header("Instructions")
    st.markdown(
        """
        1. Upload an image using the file uploader
        2. Wait for Claude 3.5 to analyze the image
        3. View the detailed description and analysis
        """
    )
    st.header("AWS Configuration")
    st.info(
        "This app uses your local AWS profile for authentication. "
        "Make sure you have configured your AWS credentials with access to Amazon Bedrock."
    )

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Process the uploaded image
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Uploaded Image")
        st.image(image, use_column_width=True)
    
    # Convert the image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    # Analysis button
    if st.button("Analyze Image", key="analyze"):
        with st.spinner("Claude 3.5 is analyzing your image..."):
            try:
                # Get image description from Claude 3.5 via Bedrock
                description = get_image_description(img_str)
                
                with col2:
                    st.subheader("Image Analysis")
                    st.markdown(description)
                
                # Save the results
                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
                if "AccessDeniedException" in str(e):
                    st.warning("Please check your AWS credentials and Bedrock access permissions.")
else:
    # Display sample images when no file is uploaded
    st.info("Please upload an image to analyze.")
