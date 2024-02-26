"""Ingest helper module."""

import os
import re
from urllib.parse import urlparse

from app.core.config import config


class IngestHelper:
    """Ingest helper class."""

    @staticmethod
    def allowed_file(filename: str):
        """Check if a file is allowed based on its extension."""
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
        )

    @staticmethod
    def check_file_size(file_content: bytes):
        """Check if a file exceeds the maximum allowed size."""
        return len(file_content) > config.MAX_FILE_SIZE

    @staticmethod
    def check_file_exists(file_path: str):
        """Check if a file exists."""
        return os.path.exists(file_path)

    @staticmethod
    def save_to_folder(file_content: bytes, file_path: str):
        """Save a file to a folder."""
        with open(file_path, "wb") as f:
            f.write(file_content)

    @staticmethod
    def get_all_files() -> list[str]:
        """Get all files in the local data folder."""
        return os.listdir(config.LOCAL_DATA_FOLDER)

    def delete_file(self, file_name: str) -> bool:
        """Delete a file from the local data folder."""
        file_path = os.path.join(config.LOCAL_DATA_FOLDER, file_name)

        if self.check_file_exists(file_path):
            os.remove(file_path)
            return True

        return False

    @staticmethod
    def strip_consecutive_newlines(text: str) -> str:
        """Strip consecutive newlines from a text."""
        return re.sub(r"\s*\n\s*", "\n", text)

    @staticmethod
    def is_file_link(url: str) -> bool:
        """Check if a URL is a link to a file."""
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path.endswith(
            (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", "txt")
        ):
            return True
        return False

    @staticmethod
    def is_youtube_video(url: str) -> bool:
        """
        Returns True if the given URL is a video on YouTube, False otherwise.
        """
        # Regular expression pattern to match YouTube video URLs
        youtube_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([^\s&]+)"

        # Match the pattern against the URL
        match = re.match(youtube_pattern, url)

        # If there's a match, it's a YouTube video URL
        if match:
            return True

        # Otherwise, it's not a YouTube video URL
        return False
