from pathlib import Path
from auto_fiddler.download import Downloader


def main():
    # Paths to YAML files containing the sites
    abc_sites_file = Path("./auto_fiddler/abc.yaml")
    txt_sites_file = Path("./auto_fiddler/txt.yaml")

    # Define the target folder for downloads
    save_path = Path("./music_files")

    # Create a FileDownloader instance
    downloader = Downloader(target_folder=save_path, num_threads=2)

    # Download and classify files from ABC sites
    print("Downloading ABC files...")
    downloader.download_sites_from_yaml(abc_sites_file, ".abc")

    # Download and classify files from TXT sites
    print("Downloading TXT files...")
    downloader.download_sites_from_yaml(txt_sites_file, ".txt")

    # Remove Duplicate Files
    print("Removing Duplicate Files")
    downloader.remove_duplicates()

    # Classify downloaded files
    print("Classifying downloaded files...")
    downloader.classify_all_files(".abc")
    downloader.classify_all_files(".txt")


if __name__ == "__main__":
    main()
