import streamlit as st
from PIL import Image, ImageOps
import os
import requests
from io import BytesIO

# Function to process the image
def process_image(image):
    # Ensure the image is in RGB mode
    image = image.convert("RGB")
    # Resize and make the image square
    size = (1000, 1000)
    background_color = (255, 255, 255)
    # Create a new image with white background
    background = Image.new('RGB', size, background_color)
    # Calculate the ratio and size for resizing
    ratio = min(size[0] / image.width, size[1] / image.height)
    new_size = (int(image.width * ratio), int(image.height * ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)
    # Paste the resized image onto the background
    background.paste(resized_image, ((size[0] - new_size[0]) // 2, (size[1] - new_size[1]) // 2))
    return background

# Create directories if not exist
os.makedirs('./temp', exist_ok=True)
os.makedirs('./square', exist_ok=True)

st.title("Image Upload and Process App")

# Option to upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Option to enter URL
image_url = st.text_input("Or enter an image URL...")

image = None
image_source = None

# Check if an image is uploaded
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_source = uploaded_file.name

# Check if a URL is provided
elif image_url:
    try:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image_source = os.path.basename(image_url)
    except Exception as e:
        st.error(f"Error fetching the image: {e}")

if image is not None:
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Process the image
    processed_image = process_image(image)

    # Save the processed image to the square directory
    processed_image_path = os.path.join('./square', f"{os.path.splitext(image_source)[0]}-sq.jpg")
    processed_image.save(processed_image_path)

    st.image(processed_image, caption='Processed Image.', use_column_width=True)

    # Provide a download button for the processed image
    with open(processed_image_path, "rb") as file:
        btn = st.download_button(
            label="Download Processed Image",
            data=file,
            file_name=f"{os.path.splitext(image_source)[0]}-sq.jpg",
            mime="image/jpeg"
        )

# Clean up temp directory
if os.path.exists('./temp'):
    for file in os.listdir('./temp'):
        os.remove(os.path.join('./temp', file))
