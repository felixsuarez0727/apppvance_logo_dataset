import os
from PIL import Image

# Function to resize .jpg images horizontally and vertically
def resize_images(input_folder, output_folder, new_width, new_height):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.endswith(".jpg"):  # Adjust the file extension if needed
                image_path = os.path.join(input_folder, filename)
                try:
                    with Image.open(image_path) as img:
                        # Resize the image using PIL.Image.LANCZOS resampling
                        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                        # Save the resized image
                        output_path = os.path.join(output_folder, filename)
                        resized_img.save(output_path, "JPEG")
                        print(f"Resized {image_path} and saved as {output_path}")
                except Exception as e:
                    # Delete the image if resizing fails
                    os.remove(image_path)
                    print(f"Deleted {image_path} due to resizing error: {e}")
    except Exception as e:
        print(f"Error resizing images: {e}")

   
