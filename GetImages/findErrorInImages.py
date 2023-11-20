import os
from PIL import Image




def convert_and_resize_images(root_folder, results_folder, t_size):
    problematic_images = []

    def convert_and_save_image(src_filename, dest_filename):
        try:
            image_file = Image.open(src_filename)
            
            # Check if the image is in CMYK mode
            if image_file.mode == "CMYK":
                # Add the path of the problematic image to the list
                problematic_images.append(src_filename)
                # Convert the image to RGB mode
                image_file = image_file.convert("RGB")
            
            # Resize the image
            image_file.thumbnail((t_size, t_size), Image.LANCZOS)  # Updated resampling filter
            
            # Save the image as JPG in the specified destination folder
            image_file.save(dest_filename, "JPEG", optimize=True)
            return True
        except (IOError, IndexError, TypeError) as e:
            return False

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            src_filename = os.path.join(foldername, filename)
            
            # Calculate the destination path while preserving folder structure
            dest_folder = os.path.join(results_folder, os.path.relpath(foldername, root_folder))
            os.makedirs(dest_folder, exist_ok=True)
            dest_filename = os.path.join(dest_folder, filename)
            
            if not convert_and_save_image(src_filename, dest_filename):
                problematic_images.append(src_filename)

    if problematic_images:
        print("Problematic images in CMYK mode:")
        for image in problematic_images:
            print(image)
    else:
        print("No problematic images found in CMYK mode.")


