"""auto-fiddler: for downloading and analyzing abc fiddle tunes"""

from pathlib import Path
from auto_fiddler.data_collection.downloader import FileDownloader


url = "https://nigelgatherer.com/tunes/abc/abc1.html"
path = Path("./downloaded_files")
downloader = FileDownloader(url, path)
downloader.download_files(".abc")
