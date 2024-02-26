"""
Remote file reader.

A loader that fetches an arbitrary remote page or file by URL and parses its contents.

"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from llama_index.core import SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from llama_index.readers.youtube_transcript import YoutubeTranscriptReader

from app.api.helpers.readers.web_reader import WebBaseLoader
from app.api.helpers.ingest_helper import IngestHelper
from app.logger.logger import custom_logger

ingest_helper = IngestHelper()


class RemoteReader(BaseReader):
    """General reader for any remote page or file."""

    def __init__(
        self,
        *args: Any,
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        **kwargs: Any,
    ) -> None:
        """Init params."""
        super().__init__(*args, **kwargs)

        self.file_extractor = file_extractor

    def load_data(self, url: str) -> List[Document]:
        """Parse whatever is at the URL."""
        import tempfile
        from urllib.parse import urlparse
        from urllib.request import Request, urlopen

        extra_info = {"source": url}

        req = Request(url, headers={"User-Agent": "Magic Browser"})
        custom_logger.debug(f"Fetching")
        result = urlopen(req)
        url_type = result.info().get_content_type()
        documents = []
        if ingest_helper.is_youtube_video(url):
            youtube_reader = YoutubeTranscriptReader()
            documents = youtube_reader.load_data(ytlinks=[url], languages=["en", "vi"])

            for doc in documents:
                doc.extra_info = extra_info

        elif url_type == "text/plain":
            text = "\n\n".join([str(el.decode("utf-8-sig")) for el in result])
            documents = [Document(text=text, extra_info=extra_info)]

        elif ingest_helper.is_file_link(url):
            suffix = Path(urlparse(url).path).suffix
            with tempfile.TemporaryDirectory() as temp_dir:
                filepath = f"{temp_dir}/temp{suffix}"
                with open(filepath, "wb") as output:
                    output.write(result.read())
                loader = SimpleDirectoryReader(
                    temp_dir,
                    file_metadata=(lambda _: extra_info),
                    file_extractor=self.file_extractor,
                )
                documents = loader.load_data()

        else:
            custom_logger.debug(f"Fetching {url}")
            loader = WebBaseLoader(web_path=url)
            documents = loader.load()

        return documents
