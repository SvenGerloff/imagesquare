from wand.image import Image
from wand.exceptions import WandException
import os

# Define the file names
input_filename = '51n8qFkGYUL._AC_.jbg'
output_filename = '51n8qFkGYUL._AC_resized.jbg'

try:
    # Open the image file
    with Image(filename=input_filename) as img:
        # Resize the image
        img.resize(200, 300)

        # Save the image to the same folder with a new name
        img.save(filename=output_filename)

    print(f"Image processing completed. The output image is saved as {output_filename}.")

except WandException as e:
    print(f"An error occurred: {e}")

except FileNotFoundError:
    print(f"The file {input_filename} does not exist.")
