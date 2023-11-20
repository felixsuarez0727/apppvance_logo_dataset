import os

def cleanup_large_images(folder_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    # List of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            # Get the file extension
            file_extension = os.path.splitext(filename)[1].lower()

            # Check if the file extension is in the list of image extensions
            if file_extension in image_extensions:
                # Get the size of the file in bytes
                file_size = os.path.getsize(file_path)

                # Check if the file size is greater than 50KB (50 * 1024 bytes)
                if file_size > 50 * 1024:
                    try:
                        # Delete the file
                        os.remove(file_path)
                        print(f"Deleted: {filename}")
                    except Exception as e:
                        print(f"Error deleting {filename}: {e}")

    print("Deletion process completed.")


