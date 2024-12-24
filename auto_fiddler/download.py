"""A module to manage the downloading of files"""

import os
import hashlib
import shutil
from pathlib import Path
from threading import Thread, Semaphore
from typing import List
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup
from music21 import converter, stream


class Downloader:
    """Class for downloading and classifying music files."""

    def __init__(
        self, target_folder: Path = Path("./downloads"), num_threads: int = 1
    ) -> None:
        """
        Initializes the FileDownloader class.

        Args:
            target_folder (Path, optional): Folder to download files to. Defaults to "./downloads".
            num_threads (int, optional): Number of threads to use for downloading.
                Defaults to 1 (sequential download).
        """
        self.target_folder = target_folder
        self.num_threads = num_threads
        os.makedirs(self.target_folder, exist_ok=True)

    def download_sites_from_yaml(self, yaml_file: Path, file_extension: str) -> None:
        """
        Loads site URLs from a YAML file and downloads all files.

        Args:
            yaml_file (Path): Path to the YAML file.
            file_extension (str): File extension of files to download.
        """
        try:
            # Load the YAML file
            with open(yaml_file, "r") as f:
                data = yaml.safe_load(f)
                sites = list(data.values())[0]  # Extract the list of sites

            # Download files from each site
            for site in sites:
                print(f"Processing site: {site}")
                self.download_files(site, file_extension)
        except Exception as e:
            print(f"Failed to process YAML file {yaml_file}: {e}")

    def get_file_links(self, source_url: str, file_extension: str) -> List[str]:
        """
        Gets a list of all files with the specified extension on the webpage.

        Args:
            source_url (str): The URL of the website to scrape.
            file_extension (str): File extension to search for.

        Returns:
            List[str]: List of downloadable file URLs.
        """
        try:
            response = requests.get(source_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            return [
                urljoin(source_url, link["href"])
                for link in links
                if link["href"].endswith(file_extension)
            ]

        except requests.RequestException as e:
            print(f"Error fetching links from {source_url}: {e}")
            return []

    def _download_file(self, link: str) -> None:
        """Downloads a single file from a given URL."""
        file_name = self.target_folder / link.split("/")[-1]
        try:
            response = requests.get(link, timeout=10)
            response.raise_for_status()
            with open(file_name, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {file_name} from {link}")

        except requests.RequestException as e:
            print(f"Failed to download {link}: {e}")

    def download_files(self, source_url: str, file_extension: str) -> None:
        """
        Downloads all files with a given extension from the specified source URL.

        Args:
            source_url (str): The URL to download files from.
            file_extension (str): File extension of files to download.
        """
        file_links = self.get_file_links(source_url, file_extension)
        if not file_links:
            print(
                f"No files found with the extension '{file_extension}' at {source_url}."
            )
            return

        if self.num_threads == 1:
            for link in file_links:
                self._download_file(link)
        else:
            self._download_files_multithreaded(file_links)

    def _download_files_multithreaded(self, file_links: List[str]) -> None:
        """Handles multithreaded downloading of files."""
        semaphore = Semaphore(self.num_threads)
        threads = []

        for link in file_links:
            semaphore.acquire()
            thread = Thread(
                target=self._download_with_semaphore, args=(link, semaphore)
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def _download_with_semaphore(self, link: str, semaphore: Semaphore) -> None:
        """Downloads a file and releases the semaphore after completion."""
        try:
            self._download_file(link)
        finally:
            semaphore.release()

    def classify(self, file_path: Path) -> None:
        """
        Classifies and moves the music file to a specific folder based on its music21 type.

        Args:
            file_path (Path): Path to the music file to classify.
        """
        try:
            parsed = converter.parse(file_path, format="abc")
            target_folder = self.target_folder / "others"  # Default folder

            if isinstance(parsed, stream.Score):
                target_folder = self.target_folder / "tunes"
            elif isinstance(parsed, stream.Opus):
                target_folder = self.target_folder / "collections"
            elif parsed is None:
                target_folder = self.target_folder / "unknown"

            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), target_folder / file_path.name)
            print(f"Moved {file_path} to {target_folder}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            target_folder = self.target_folder / "unknown"
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), target_folder / file_path.name)
            print(f"Moved {file_path} to {target_folder}")

    def classify_all_files(self, extension: str = ".mxl") -> None:
        """
        Classifies all music files in the target folder based on their music21 type.

        Args:
            extension (str, optional): File extension of files to classify. Defaults to ".mxl".
        """
        for file_path in self.target_folder.rglob(f"*{extension}"):
            if file_path.is_file():
                self.classify(file_path)

    def calculate_hash(self, file_path: Path) -> str:
        """
        Calculates the SHA-256 hash of a file's content.

        Args:
            file_path (Path): Path to the file.

        Returns:
            str: SHA-256 hash of the file content.
        """
        hash_func = hashlib.sha256()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def remove_duplicates(self) -> None:
        """
        Removes duplicate files in the target folder based on file content hash.
        """
        seen_hashes = {}
        removed_files_count = 0

        for file_path in self.target_folder.rglob("*"):
            if file_path.is_file():
                file_hash = self.calculate_hash(file_path)

                if file_hash in seen_hashes:
                    print(f"Removing duplicate file: {file_path}")
                    os.remove(file_path)
                    removed_files_count += 1
                else:
                    seen_hashes[file_hash] = file_path

        print(f"Duplicate removal complete. {removed_files_count} files removed.")
