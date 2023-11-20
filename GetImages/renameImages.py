import os
import glob

def rename_images(folder_path, image_extensions = ['jpg']):
    # Use glob to search for files with the specified extensions
    image_files = []
    for extension in image_extensions:
        pattern = os.path.join(folder_path, f'*.{extension}')
        image_files.extend(glob.glob(pattern))

    # Helper function to check if a file exists
    def file_exists(file_path):
        return os.path.isfile(file_path)

    # Rename the images to sequential numbers (1, 2, 3, 4, ...)
    for i, old_image_path in enumerate(image_files, start=1):
        image_extension = os.path.splitext(old_image_path)[-1]
        new_image_path = os.path.join(folder_path, f'{i}{image_extension}')

        try:
            os.rename(old_image_path, new_image_path)
            print(f'Renamed: {old_image_path} to {new_image_path}')
        except Exception as e:
            print(f"Error renaming {old_image_path}: {e}")
            if "already exists" in str(e):
                # If the file with the new name already exists, use a different naming format
                for j in range(1, len(image_files) + 1):
                    alternative_new_image_path = os.path.join(folder_path, f'image_{j:03d}{image_extension}')
                    if not file_exists(alternative_new_image_path):
                        os.rename(old_image_path, alternative_new_image_path)
                        print(f'Renamed to alternative name: {old_image_path} to {alternative_new_image_path}')
                        break

    # Optional: You can also return the total number of image files found
    return len(image_files)


    
