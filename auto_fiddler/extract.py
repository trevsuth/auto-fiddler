"""A module for working with ABC files"""

import re
from pathlib import Path
from typing import Optional, Dict


class ABCMusicFile:
    """Class for working with ABC music files"""

    def __init__(self, file_path: Path) -> None:
        """Initializes with the path to an ABC file

        Args:
            file_path (Path): Path to the ABC music file
        """
        self.file_path = file_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        """Reads the content of the ABC file

        Returns:
            str: Content of the file as a single string
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _get_metadata_field(self, field: str) -> Optional[str]:
        """Extracts a specified metadata field from the file content

        Args:
            field (str): The field identifier (e.g., 'T' for Title)

        Returns:
            Optional[str]: The value of the specified field or None if not found
        """
        pattern = rf"^{field}:(.*)$"
        match = re.search(pattern, self.content, re.MULTILINE)
        return match.group(1).strip() if match else None

    def get_title(self) -> Optional[str]:
        """Extracts the title of the tune (T: field)"""
        return self._get_metadata_field("T")

    def get_composer(self) -> Optional[str]:
        """Extracts the composer of the tune (C: field)"""
        return self._get_metadata_field("C")

    def get_key(self) -> Optional[str]:
        """Extracts the key of the tune (K: field)"""
        return self._get_metadata_field("K")

    def get_meter(self) -> Optional[str]:
        """Extracts the meter of the tune (M: field)"""
        return self._get_metadata_field("M")

    def get_tempo(self) -> Optional[str]:
        """Extracts the tempo of the tune (Q: field)"""
        return self._get_metadata_field("Q")

    def get_default_note_length(self) -> Optional[str]:
        """Extracts the default note length of the tune (L: field)"""
        return self._get_metadata_field("L")

    def get_all_metadata(self) -> Dict[str, Optional[str]]:
        """Extracts all common metadata fields from the tune

        Returns:
            Dict[str, Optional[str]]: Dictionary of metadata fields and values
        """
        return {
            "Title": self.get_title(),
            "Composer": self.get_composer(),
            "Key": self.get_key(),
            "Meter": self.get_meter(),
            "Tempo": self.get_tempo(),
            "Default Note Length": self.get_default_note_length(),
        }

    def get_tune(self) -> str:
        """Extracts the tune notation (skipping metadata)

        Returns:
            str: The tune notation
        """
        # Find the starting line of the tune with the "K:" (Key) field
        tune_start = re.search(r"^K:.*$", self.content, re.MULTILINE)
        if not tune_start:
            return ""

        # Extract tune content after the "K:" field line
        tune_position = tune_start.end()
        return self.content[tune_position:].strip()


# Example usage:
if __name__ == "__main__":
    file_path = Path("path/to/your/tune.abc")
    abc_file = ABCMusicFile(file_path)
    print("Title:", abc_file.get_title())
    print("Composer:", abc_file.get_composer())
    print("Key:", abc_file.get_key())
    print("Tune notation:", abc_file.get_tune())
