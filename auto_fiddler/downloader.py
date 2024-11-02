import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class FileDownloader:
    def __init__(self, base_url, download_folder="downloads"):
        self.base_url = base_url
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)

    def get_file_links(self, file_extension):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            file_links = [
                urljoin(self.base_url, link["href"])
                for link in links
                if link["href"].endswith(file_extension)
            ]
            return file_links

        except requests.RequestException as e:
            print(f"Error fetching links: {e}")
            return []

    def download_files(self, file_extension):
        file_links = self.get_file_links(file_extension)
        if not file_links:
            print("No files found with the given extension.")
            return

        for link in file_links:
            file_name = os.path.join(self.download_folder, link.split("/")[-1])
            try:
                response = requests.get(link)
                response.raise_for_status()

                with open(file_name, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {file_name}")

            except requests.RequestException as e:
                print(f"Failed to download {link}: {e}")


# Usage example:
# downloader = FileDownloader("https://example.com/files", "downloaded_files")
# downloader.download_files(".pdf")
