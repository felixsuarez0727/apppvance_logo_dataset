import os
from PIL import Image

def cleanup_corrupted_images(folder_path):
    def is_valid_jpg(image_path):
        try:
            with Image.open(image_path) as img:
                img.verify()
                return True
        except (IOError, SyntaxError):
            return False

    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):  # Adjust the file extension if needed
            image_path = os.path.join(folder_path, filename)
            if not is_valid_jpg(image_path):
                print(f"Deleting corrupted image: {image_path}")
                os.remove(image_path)