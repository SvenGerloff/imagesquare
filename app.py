import streamlit as st
import os
import requests
from subprocess import run
from io import BytesIO

# Function to process the image using the bash script
def process_image_with_wand(image_path, output_dir, output_filename):
    script_path = './process_image.sh'
    run(['bash', script_path, image_path, output_dir, output_filename])

# Create directories if not exist
os.makedirs('./temp', exist_ok=True)
os.makedirs('./square', exist_ok=True)

st.title("Image Upload and Process App")

# Choose input method
input_method = st.radio("Select input method:", ("Upload Image", "Enter Image URL"))

image_path = None
image_source = None

# Handle image upload
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_path = os.path.join('./temp', uploaded_file.name)
        with open(image_path, 'wb') as file:
            file.write(uploaded_file.getbuffer())
        image_source = uploaded_file.name

# Handle image URL input
elif input_method == "Enter Image URL":
    image_url = st.text_input("Enter an image URL...")
    if image_url:
        try:
            response = requests.get(image_url)
            image_path = os.path.join('./temp', os.path.basename(image_url))
            with open(image_path, 'wb') as file:
                file.write(response.content)
            image_source = os.path.basename(image_url)
        except Exception as e:
            st.error(f"Error fetching the image: {e}")

if image_path is not None:
    st.image(image_path, caption='Uploaded Image.', use_column_width=True)

    # Process the image
    output_filename = f"{os.path.splitext(image_source)[0]}-sq.jpg"
    process_image_with_wand(image_path, './square', output_filename)

    # Path to the processed image
    processed_image_path = os.path.join('./square', output_filename)

    # Display the processed image
    st.image(processed_image_path, caption='Processed Image.', use_column_width=True)

    # Provide a download button for the processed image
    with open(processed_image_path, "rb") as file:
        btn = st.download_button(
            label="Download Processed Image",
            data=file,
            file_name=output_filename,
            mime="image/jpeg"
        )

# Clean up temp directory
if os.path.exists('./temp'):
    for file in os.listdir('./temp'):
        os.remove(os.path.join('./temp', file))
