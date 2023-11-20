import os
import requests
from concurrent import futures
from bing_images import bing
from duckduckgo_search import ddg_images

# Function to fetch image URLs from DuckDuckGo
def fetch_ddg_image_urls(query, limit=10):
    results = ddg_images(query, max_results=limit)
    urls = [result['image'] for result in results]
    print("{} images from DuckDuckGo Images.".format(len(urls)))
    return urls

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
            return None, None  # Return placeholders for both URL and file path
        
        # Check if the URL ends with .jpg or .png
        if not (url.lower().endswith('.jpg') or url.lower().endswith('.png')):
            print(f"Skipping {url} because it's not a .jpg or .png file")
            return None, None  # Return placeholders for both URL and file path
        
        # Download the image with a timeout
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            # Get the image number from the total downloaded
            image_number = len(os.listdir(output_dir)) + 1
            file_extension = '.jpg' if url.lower().endswith('.jpg') else '.png'
            file_path = os.path.join(output_dir, f"image_{image_number}{file_extension}")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {url} as image_{image_number}{file_extension}")
            return url, file_path
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            return None, None  # Return placeholders for both URL and file path
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None, None  # Return placeholders for both URL and file path


if __name__ == "__main__":
    # Step 1: Get user input for the search query
    query = input("Enter the search query for images: ")
    num_images = int(input("Enter the number of images you want to download: "))  # Ask for the number of images
    
    downloaded_count = 0
    with futures.ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        while downloaded_count < num_images:
            # Step 2: Fetch URLs of images from Bing
            bing_image_urls = fetch_and_print_image_urls(query, limit=100, file_type='jpg', filters='', extra_query_params=f'&first={downloaded_count + 1}')
            
            # Step 3: Fetch URLs of images from DuckDuckGo Images
            ddg_image_urls = fetch_ddg_image_urls(query, limit=100)
            
            # Combine both sets of image URLs
            image_urls = bing_image_urls + ddg_image_urls
            
            # Step 4: Download the images concurrently while filtering by file size and file type (not more than 50KB and .jpg)
            results = list(executor.map(lambda url: download_image_with_timeout(url, output_dir="outputs", max_file_size=50 * 1024, timeout=10), image_urls))
            
            # Write the URLs to a text file
            with open('downloaded_images.txt', 'a') as file:
                for result in results:
                    if result is not None:
                        url, file_path = result
                        if file_path is not None:
                            file.write(f"{url}\n")
                            print(f"Saved URL: {url}")


            
            # Count the successful downloads and update the total count
            downloaded_count += len([url for url, _ in results if url is not None])
            print(f"Downloaded {downloaded_count} images based on the search query.")
