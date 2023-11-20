import os
import hashlib
from collections import defaultdict

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path, block_size=8192):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to find and delete duplicate images
def delete_duplicate_images(folder_path):
    try:
        # Create a dictionary to store hashes and corresponding file paths
        hash_to_files = defaultdict(list)

        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg"):  # Adjust the file extension if needed
                file_path = os.path.join(folder_path, filename)
                md5_hash = calculate_md5(file_path)
                hash_to_files[md5_hash].append(file_path)

        # Delete duplicate images, keeping only one copy of each
        for hash, files in hash_to_files.items():
            if len(files) > 1:
                print(f"Found duplicate images with hash {hash}:")
                for i, file_path in enumerate(files):
                    if i > 0:
                        print(f"Deleting: {file_path}")
                        os.remove(file_path)

        print("Finished deleting duplicate images.")
    except Exception as e:
        print(f"Error deleting duplicate images: {e}")


    
