"""
Modules for transforming ABC files into music21 stream objects

Modules:
    CreateCorpus
"""

import os
from pathlib import Path
import shutil
from typing import List

from music21 import converter, stream


class CreateCorpus:
    def __init__(self, target_folder: Path) -> None:
        self.target_folder = target_folder
        os.makedirs(self.target_folder, exist_ok=True)

    def _iterate_through_folder(
        self, source_folder: Path, recursive: bool = False
    ) -> List[Path]:
        """
        Iterates through files in a folder and returns a list of file paths.

        Args:
            source_folder (Path): The directory to iterate through.
            recursive (bool): If True, includes files in subdirectories. Default is False.

        Returns:
            List[Path]: A list of file paths found in the folder.
        """
        if not source_folder.is_dir():
            raise ValueError(
                f"The provided path '{source_folder}' is not a valid directory."
            )

        # Use globbing for recursive or non-recursive iteration
        pattern = "**/*" if recursive else "*"

        # Collect files
        file_paths = [path for path in source_folder.glob(pattern) if path.is_file()]

        return file_paths

    def extract_tunes_from_collections(self, source_file: Path, keep_original: bool = True) -> None:
        """Given a Music21.opus file, will copy each tune from the file into self.target_folder

        Args:
            source_file (Path): a music21.stream.opus file
            keep_original (Bool): If true, original collection file will be preserved.
                If False, it will be deleted.  Defaults to True
        """
        
        with source_file as collection:
            parsed_file = converter.parse(source_file, format="abc")