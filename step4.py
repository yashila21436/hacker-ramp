import os
import requests
import re
import time
from tqdm import tqdm

def sanitize_filename(filename):
    # Remove or replace invalid characters and shorten filename if too long
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized[:150]  # Limit the length to avoid path length issues

def download_images_from_file(file_path, download_folder):
    # Create the download folder if it does not exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Read the file and get the URLs
    with open(file_path, 'r') as file:
        urls = file.readlines()

    failed_downloads = []
    
    # Initialize tqdm for progress bar
    progress_bar = tqdm(total=len(urls), desc="Processing URLs", unit="URL")

    # Download each image
    for idx, url in enumerate(urls):
        url = url.strip()
        try:
            start_time = time.time()
            response = requests.get(url, stream=True, timeout=600)  # Timeout set to 10 minutes (600 seconds)
            response.raise_for_status()
            
            # Get the image file name from the URL
            filename = os.path.basename(url).split('?')[0]  # Ignore URL parameters
            filename = sanitize_filename(filename)
            filepath = os.path.join(download_folder, filename)
            
            # Write the image to the file
            with open(filepath, 'wb') as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)
            
            print(f"Downloaded {url} to {filepath}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")
            failed_downloads.append(url)
        except OSError as e:
            print(f"Error saving {url} to {filepath}: {e}")
            failed_downloads.append(url)
        except requests.exceptions.Timeout:
            print(f"Timeout error: Failed to download {url} within 10 minutes")
            failed_downloads.append(url)
        
        # Update progress bar
        progress_bar.update(1)

    progress_bar.close()

    if failed_downloads:
        print("\nFailed to download the following images:")
        for url in failed_downloads:
            print(url)

if __name__ == "__main__":
    file_path = r'C:\Users\yaror\OneDrive\Desktop\Myntra 13th July\2022_image_urls.txt'  # Path to the text file with URLs
    download_folder = r'C:\Users\yaror\OneDrive\Desktop\Myntra 13th July\2022_downloaded_images'  # Folder to save the images
    download_images_from_file(file_path, download_folder)
