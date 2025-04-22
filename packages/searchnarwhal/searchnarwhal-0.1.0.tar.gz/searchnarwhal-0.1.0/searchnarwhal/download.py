# searchnarwhal/download.py

import os
import requests
from tkinter import messagebox

# Get the user's Downloads folder
def get_download_folder():
    home_dir = os.path.expanduser("~")
    download_folder = os.path.join(home_dir, "Downloads")
    return download_folder

def download(url):
    try:
        # Create the downloads folder if it doesn't exist
        download_folder = get_download_folder()
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Get the filename from the URL (last part of the URL)
        filename = url.split("/")[-1]
        file_path = os.path.join(download_folder, filename)

        # Download the file
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for HTTP errors

        with open(file_path, 'wb') as file:
            file.write(response.content)

        messagebox.showinfo("Download Complete", f"File downloaded to: {file_path}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Download Error", f"Error downloading {url}: {e}")
