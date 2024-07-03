import streamlit as st
import os
import requests
from io import BytesIO
from zipfile import ZipFile
from PIL import Image, ImageOps
import uuid
import subprocess
import sys

try:
    from streamlit_extras.stylable_container import stylable_container
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'streamlit_extras'])
finally:
    from streamlit_extras.stylable_container import stylable_container

# Function to process the image using Pillow
def process_image(image_path, output_dir, output_filename):
    with Image.open(image_path) as img:
        img = ImageOps.contain(img, (600, 600))
        background = Image.new('RGB', (1000, 1000), 'white')
        offset = ((1000 - img.width) // 2, (1000 - img.height) // 2)
        background.paste(img, offset)
        output_path = os.path.join(output_dir, output_filename)
        background.save(output_path, format='JPEG')

# Create directories if not exist
os.makedirs('./temp', exist_ok=True)
os.makedirs('./square', exist_ok=True)

st.set_page_config(page_title="Square Product Images",
                   layout="centered",
                   page_icon="📸")

st.title("📸 Square Product Images")
st.write("""
    Welcome to the Square Product Images app! Follow these steps to process your images:

    1. **Enter Image URLs:** Provide the URLs of the images you want to process, one per line.
    2. **Process Images:** Click on the **Process Image(s)** button to start processing the images.
    3. **Download Images:** 
       - To download all processed images as a zip file, click on the **Download All Images as Zip** button.
       - To download individual images, use the **Download Image** button below each image.
    4. **Reset:** To add new images, click the **Reset** button to clear the previous inputs.
    5. **Error Handling:** If you encounter any unexpected error messages, please reload the page and try again.
""")

# Initialize session state for image URLs and processed image paths
if 'image_urls' not in st.session_state:
    st.session_state.image_urls = ""
if 'processed_image_paths' not in st.session_state:
    st.session_state.processed_image_paths = []

# Reset functionality
def reset():
    st.session_state.image_urls = ""
    st.session_state.processed_image_paths = []
    if os.path.exists('./temp'):
        for file in os.listdir('./temp'):
            os.remove(os.path.join('./temp', file))
    if os.path.exists('./square'):
        for file in os.listdir('./square'):
            os.remove(os.path.join('./square', file))
    st.rerun()

# Handle image URL input
st.session_state.image_urls = st.text_area("Enter image URLs (one per line)...", value=st.session_state.image_urls)
image_paths = []
image_sources = []

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
    with stylable_container(
            key="green_button",
            css_styles="""
              button {
                  background-color: #20D599;
                  color: black;
                  border-radius: 20px;
              }
              """,
    ):
        process_clicked = st.button("⚙️ Process Image(s)", help="Click to process the images from the URLs.")
with col2:
    with stylable_container(
            key="red_button",
            css_styles="""
                  button {
                      background-color: #F95F68;
                      color: black;
                      border-radius: 20px;
                  }
                  """,
    ):
        reset_clicked = st.button("❌ Reset", help="Click to reset all inputs and clear the results.")

if process_clicked:
    if image_paths:
        st.write("Processing your images...")
        progress_bar = st.progress(0)
        processed_image_paths = []

        # Process each image
        for i, (image_path, image_source) in enumerate(zip(image_paths, image_sources)):
            output_filename = f"{str(uuid.uuid4())}.jpg"
            try:
                process_image(image_path, './square', output_filename)
                processed_image_path = os.path.join('./square', output_filename)
                if os.path.exists(processed_image_path):  # Check if the file was created
                    processed_image_paths.append((processed_image_path, output_filename))
                else:
                    st.error(f"Error: Processed file {processed_image_path} does not exist.")
            except Exception as e:
                st.error(f"Error processing the image {image_source}: {e}")

            progress_bar.progress((i + 1) / len(image_paths))

        st.session_state.processed_image_paths = processed_image_paths
        st.success("Image processing completed successfully!")
    else:
        st.warning("Please enter image URLs before processing.")

if reset_clicked:
    reset()

# Display processed images and individual download buttons if available
if st.session_state.processed_image_paths:
    processed_image_paths = st.session_state.processed_image_paths
    cols = st.columns(4)
    for idx, (processed_image_path, output_filename) in enumerate(processed_image_paths):
        try:
            image = Image.open(processed_image_path)
            with cols[idx % 4]:
                st.image(image, use_column_width=True, caption=output_filename)
                with open(processed_image_path, "rb") as file:
                    with stylable_container(
                            key=f"blue_button_{output_filename}",
                            css_styles="""
                                  button {
                                      background-color: #227AF7;
                                      color: black;
                                      border-radius: 20px;
                                  }
                                  """,
                    ):
                        st.download_button(
                            label="📥 Download Image",
                            data=file,
                            file_name=output_filename,
                            mime="image/jpeg",
                            help="Click to download the processed image.",
                            key=f"download_button_{output_filename}"
                        )
        except FileNotFoundError:
            st.error(f"Error: File {processed_image_path} not found.")
        except Exception as e:
            st.error(f"Error displaying the image {output_filename}: {e}")

    # Show the download all button after processing images
    with col3:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            for processed_image_path, output_filename in st.session_state.processed_image_paths:
                zip_file.write(processed_image_path, os.path.basename(processed_image_path))
        zip_buffer.seek(0)
        with stylable_container(
                key="purple_button",
                css_styles="""
                      button {
                          background-color: #9F5FD9;
                          color: black;
                          border-radius: 20px;
                      }
                      """,
        ):
            download_all_clicked = st.download_button(
                    label="📦 Download All Images as Zip",
                    data=zip_buffer,
                    file_name="processed_images.zip",
                    mime="application/zip",
                    help="Click to download all processed images as a zip file.",
                    key="download_all_button"
                )

        if download_all_clicked:
            reset()

# Clean up temp directory
if os.path.exists('./temp'):
    for file in os.listdir('./temp'):
        os.remove(os.path.join('./temp', file))