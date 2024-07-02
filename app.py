import streamlit as st
import os
import requests
from subprocess import run
from io import BytesIO
from zipfile import ZipFile
from PIL import Image

# Function to process the image using the bash script
def process_image(image_path, output_dir, output_filename):
    script_path = './process_image.sh'
    run(['bash', script_path, image_path, output_dir, output_filename])

# Create directories if not exist
os.makedirs('./temp', exist_ok=True)

st.set_page_config(page_title="Square Product Images", layout="centered", page_icon="📸")

st.title("📸 Square Product Images")
st.write("""
    1. You can either upload one or more image files or enter image URLs.
    2. Click on the **Process Image(s)** button to start processing the images.
    3. After processing:
       - To download all processed images as a zip file, click on the **Download All Images as Zip** button.
       - To download individual images, use the **Download Image** button below each image.
    4. To add new images or URLs, click the **Reset** button to clear the previous inputs and results.
    5. If you encounter any unexpected error messages, please reload the page and try again.

    Have fun!
""")

# Initialize session state for image URLs and processed image paths
if 'image_urls' not in st.session_state:
    st.session_state.image_urls = ""
if 'processed_image_paths' not in st.session_state:
    st.session_state.processed_image_paths = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Reset functionality
def reset():
    st.session_state.image_urls = ""
    st.session_state.processed_image_paths = []
    st.session_state.uploaded_files = []
    if os.path.exists('./temp'):
        for file in os.listdir('./temp'):
            os.remove(os.path.join('./temp', file))
    st.rerun()

# Choose input method, default to URL input
input_method = st.radio("Select input method:", ("Upload Image", "Enter Image URL(s)"), index=1)

image_paths = []
image_sources = []

# Handle image upload
if input_method == "Upload Image":
    st.session_state.uploaded_files = st.file_uploader("Choose image(s)...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if st.session_state.uploaded_files:
        for uploaded_file in st.session_state.uploaded_files:
            image_path = os.path.join('./temp', uploaded_file.name)
            with open(image_path, 'wb') as file:
                file.write(uploaded_file.getbuffer())
            image_paths.append(image_path)
            image_sources.append(uploaded_file.name)

# Handle image URL input
elif input_method == "Enter Image URL(s)":
    st.session_state.image_urls = st.text_area("Enter image URLs (one per line)...", value=st.session_state.image_urls)
    if st.session_state.image_urls:
        for image_url in st.session_state.image_urls.splitlines():
            try:
                response = requests.get(image_url)
                image_path = os.path.join('./temp', os.path.basename(image_url))
                with open(image_path, 'wb') as file:
                    file.write(response.content)
                image_paths.append(image_path)
                image_sources.append(os.path.basename(image_url))
            except Exception as e:
                st.error(f"Error fetching the image from {image_url}: {e}")

# Buttons for processing, reset, and download
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    process_clicked = st.button("⚙️ Process Image(s)", help="Click to process the uploaded images or URLs.")
with col2:
    reset_clicked = st.button("❌ Reset", help="Click to reset all inputs and clear the results.")

if process_clicked:
    if os.path.exists('./square'):
        for file in os.listdir('./square'):
            os.remove(os.path.join('./square', file))
    if image_paths:
        st.write("Processing your images...")
        progress_bar = st.progress(0)
        processed_image_paths = []

        # Process each image
        for i, (image_path, image_source) in enumerate(zip(image_paths, image_sources)):
            output_filename = f"{os.path.splitext(image_source)[0]}-sq.jpg"
            try:
                process_image(image_path, './square', output_filename)
                processed_image_path = os.path.join('./square', output_filename)
                processed_image_paths.append((processed_image_path, output_filename))
            except Exception as e:
                st.error(f"Error processing the image {image_source}: {e}")

            progress_bar.progress((i + 1) / len(image_paths))

        st.session_state.processed_image_paths = processed_image_paths
        st.success("Image processing completed successfully!")
    else:
        st.warning("Please upload or enter image URLs before processing.")

if reset_clicked:
    reset()

# Display processed images and individual download buttons if available
if st.session_state.processed_image_paths:
    processed_image_paths = st.session_state.processed_image_paths
    cols = st.columns(4)
    for idx, (processed_image_path, output_filename) in enumerate(processed_image_paths):
        image = Image.open(processed_image_path)
        with cols[idx % 4]:
            st.image(image, use_column_width=True, caption=output_filename)
            with open(processed_image_path, "rb") as file:
                st.download_button(
                    label="📥 Download Image",
                    data=file,
                    file_name=output_filename,
                    mime="image/jpeg",
                    help="Click to download the processed image."
                )

    # Show the download all button after processing images
    with col3:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for processed_image_path, output_filename in st.session_state.processed_image_paths:
                zip_file.write(processed_image_path, os.path.basename(processed_image_path))
        zip_buffer.seek(0)
        st.download_button(
            label="📦 Download All Images as Zip",
            data=zip_buffer,
            file_name="processed_images.zip",
            mime="application/zip",
            help="Click to download all processed images as a zip file."

        )

# Clean up temp directory
if os.path.exists('./temp'):
    for file in os.listdir('./temp'):
        os.remove(os.path.join('./temp', file))
