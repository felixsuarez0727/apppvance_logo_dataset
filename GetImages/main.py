import os
import requests
from concurrent import futures
from bing_images import bing
from verifyImages import cleanup_corrupted_images
from removeBigImages import cleanup_large_images
from stretchImages import resize_images
from deleteSameImages import delete_duplicate_images
from findErrorInImages import convert_and_resize_images
from renameImages import rename_images

image_extensions = ['.jpg', '.png', '.jpeg', '.gif', '.bmp'] 


def fetch_and_print_image_urls(query, limit=10, file_type='jpg', filters='', extra_query_params=''):
    urls = bing.fetch_image_urls(query, limit=limit, file_type=file_type, filters=filters, extra_query_params=extra_query_params)
    print("{} images.".format(len(urls)))
    return urls

# Function to download an image with timeout
def download_image_with_timeout(url, output_dir, max_file_size=50 * 1024, timeout=10):
    try:
        # Check the file size before downloading
        response = requests.head(url, timeout=timeout)
        file_size = int(response.headers.get('Content-Length', 0))
        
        if file_size > max_file_size:
            print(f"Skipping {url} due to size exceeding {max_file_size} bytes")
            return None
        
        # Check if the URL ends with .jpg
        if not url.lower().endswith('.jpg'):
            print(f"Skipping {url} because it's not a .jpg file")
            return None
        
        # Download the image with a timeout
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            # Get the image number from the total downloaded
            image_number = len(os.listdir(output_dir)) + 1
            file_path = os.path.join(output_dir, f"image_{image_number}.jpg")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {url} as image_{image_number}.jpg")
            return url
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    return None


if __name__ == "__main__":
    # Ask the user for input and save it in a variable
    search_query = input("Please enter the logo you want to look for: ")

    # Now, the user's input is stored in the 'search_query' variable
    print("You want to search for:", search_query)

    # Create an output folder with the name of the search query
    output_folder = os.path.join("outputs", search_query)
    os.makedirs(output_folder, exist_ok=True)

    # Step 1: Fetch URLs of logo images with different colors
    logo_colors = ["black", "blue", "red", "green", "pink", "yellow", "white", "silver", "gold"]  # Add more colors as needed

    with futures.ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        for color in logo_colors:
            query = f"{search_query} logo {color}"
            logo_urls = fetch_and_print_image_urls(query, limit=100, file_type='jpg', filters='', extra_query_params='&first=1')

            # Step 2: Download the images concurrently while filtering by file size and file type (not more than 50KB and .jpg)
            results = list(executor.map(lambda url: download_image_with_timeout(url, output_dir=output_folder, max_file_size=50 * 1024, timeout=10), logo_urls))

            # Count the successful downloads
            downloaded_count = len([result for result in results if result is not None])
            print(f"Downloaded {downloaded_count} {search_query} logo images for {color}.")

    # Finished message after the entire process
    print("Finished fetching and downloading logo images.")

    cleanup_corrupted_images(output_folder)
    print("Finished checking and deleting corrupted images.")


    cleanup_large_images(output_folder)
    print("Finished checking and deleting large images.")

    folder_path = "outputs"  # Replace with the path to your image folder
    delete_duplicate_images(output_folder)
    print("Finished checking and deleting duplicated images.")


    results_folder = "results"  # Replace with the path to your results folder
    t_size = 100  # Adjust the thumbnail size as needed
    convert_and_resize_images(output_folder, os.path.join(output_folder, "results"), t_size)
    # convert_and_resize_images(root_folder, results_folder, t_size)

    input_folder = output_folder  # Replace with the path to your input image folder
    resized_folder = "resized"  # Replace with the path to your output image folder
    new_width = 128  
    new_height = 128  

    resize_images(input_folder, os.path.join(output_folder, "resize"), new_width, new_height)
    print("Finished resizing images in the folder.")

    
    total_images = rename_images(os.path.join(output_folder, "results"))
    # total_images = rename_images(folder_path)
    print(f'Total number of image files: {total_images}')

    def delete_images_in_folder(folder_path, image_extensions):
        try:
            # Ensure the folder exists
            if not os.path.exists(folder_path):
                print(f"The folder '{folder_path}' does not exist.")
                return

            # Validate that the folder is a directory
            if not os.path.isdir(folder_path):
                print(f"'{folder_path}' is not a directory.")
                return

            # List all files in the folder
            files = os.listdir(folder_path)

            # Filter and delete image files
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)

                # Check if the file has a valid image extension
                if any(file_name.lower().endswith(ext) for ext in image_extensions):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

            print(f"Deleted all image files in '{folder_path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    delete_images_in_folder(output_folder, image_extensions)

    
  








