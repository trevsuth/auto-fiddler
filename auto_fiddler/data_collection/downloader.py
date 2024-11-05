"""Class for downloading files from a webpage"""

import os
from pathlib import Path
from typing import List
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class FileDownloader:
    """Class for downloading files from websites"""

    def __init__(self, website: str, folder: Path = Path("downloads")) -> None:
        """initializes the class

        Args:
            website (path): Website to scan
            target_folder (str, optional): Folder to download to.
                Defaults to "downloads".
        """
        self.url = website
        self.target_folder = folder
        os.makedirs(folder, exist_ok=True)

    def get_file_links(self, file_extension: str) -> List[str]:
        """gets a list of all files referenced on a given webpage

        Args:
            file_extension (str): file extension we are looking for

        Returns:
            List[str]: list of files downloadable from the website
        """
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            file_links = [
                urljoin(self.url, link["href"])
                for link in links
                if link["href"].endswith(file_extension)
            ]
            return file_links

        except requests.RequestException as e:
            print(f"Error fetching links: {e}")
            return []

    def download_files(self, file_extension: str) -> None:
        """Downloads files with a given file extension from a website

        Args:
            file_extension (str): file extension to download
        """
        file_links = self.get_file_links(file_extension)
        if not file_links:
            print("No files found with the given extension.")
            return

        for link in file_links:
            file_name = os.path.join(self.target_folder, link.split("/")[-1])
            try:
                response = requests.get(link, timeout=10)
                response.raise_for_status()

                with open(file_name, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded: {file_name}")

            except requests.RequestException as e:
                print(f"Failed to download {link}: {e}")


if __name__ == "__main__":
    url = "https://example.com/files"
    path = Path("./downloaded_files")
    downloader = FileDownloader(url, path)
    downloader.download_files(".pdf")
