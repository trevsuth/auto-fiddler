"""auto-fiddler: for downloading and analyzing abc fiddle tunes"""

from pathlib import Path
from auto_fiddler.data_collection.downloader import FileDownloader


website = "https://nigelgatherer.com/tunes/abc/abc1.html"
path = Path("./downloaded_files")
downloader = FileDownloader(website, path)
downloader.download_files(".abc")
