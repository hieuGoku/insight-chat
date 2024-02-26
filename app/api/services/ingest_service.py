"""Ingest Service Module"""

import os
from io import BytesIO
from typing import List, Dict, Type
from pathlib import Path
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.schema import Document, TextNode, BaseNode
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.core.storage import StorageContext
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.readers import StringIterableReader
from llama_index.core.readers.base import BaseReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SimpleNodeParser, SentenceSplitter

from app.api.database.vector_db import vector_db_client
from app.api.database.execute.docs_execute import DocsExecute
from app.api.helpers.ingest_helper import IngestHelper
from app.api.helpers.readers.web_reader import WebBaseLoader
from app.api.helpers.readers.remote_reader import RemoteReader
from app.api.errors.error_message import (
    UnsupportedFileTypeError,
    FileTooLargeError,
    FileExistsError,
)
from app.core.config import config
from app.logger.logger import custom_logger

docs_execute = DocsExecute()


class IngestService:
    """Service class for ingest operations."""

    def __init__(self) -> None:
        self.ingest_helper = IngestHelper()
        self.default_file_reader_cls = self.get_file_reader_cls()
        self.vector_store = QdrantVectorStore(
            client=vector_db_client, collection_name=config.COLLECTION_NAME
        )
        self.index_store = MongoIndexStore.from_uri(
            config.MONGO_URI, db_name=config.MONGO_DB_NAME
        )
        self.doc_store = MongoDocumentStore.from_uri(
            config.MONGO_URI, db_name=config.MONGO_DB_NAME
        )
        self.index = self.get_or_create_index()

    @staticmethod
    def get_file_reader_cls() -> Dict[str, Type[BaseReader]]:
        """
        Get reader classes for different file types.

        supported file types:
        .hwp, .pdf, .docx, .pptx, .ppt, .pptm, .jpg, .png, .jpeg, .mp3, .mp4, .csv, .epub, .md, .mbox, .ipynb
        """
        try:
            from llama_index.readers.file import (
                DocxReader,
                EpubReader,
                HWPReader,
                ImageReader,
                IPYNBReader,
                MarkdownReader,
                MboxReader,
                PandasCSVReader,
                PDFReader,
                PptxReader,
                VideoAudioReader,
            )
        except ImportError:
            raise ImportError("`llama-index-readers-file` package not found")

        default_file_reader_cls: Dict[str, Type[BaseReader]] = {
            ".hwp": HWPReader,
            ".pdf": PDFReader,
            ".docx": DocxReader,
            ".pptx": PptxReader,
            ".ppt": PptxReader,
            ".pptm": PptxReader,
            ".jpg": ImageReader,
            ".png": ImageReader,
            ".jpeg": ImageReader,
            ".mp3": VideoAudioReader,
            ".mp4": VideoAudioReader,
            ".csv": PandasCSVReader,
            ".epub": EpubReader,
            ".md": MarkdownReader,
            ".mbox": MboxReader,
            ".ipynb": IPYNBReader,
        }
        return default_file_reader_cls

    def ingest_file(self, file_content: BytesIO, file_name: str) -> List[Document]:
        """Ingest a file into the index."""

        if not self.ingest_helper.allowed_file(file_name):
            raise ValueError(UnsupportedFileTypeError)

        if self.ingest_helper.check_file_size(file_content):
            raise ValueError(FileTooLargeError)

        file_path = os.path.join(config.LOCAL_DATA_FOLDER, file_name)
        if self.ingest_helper.check_file_exists(file_path):
            raise ValueError(FileExistsError)

        self.ingest_helper.save_to_folder(file_content, file_path)

        documents = self.convert_file_to_docs(file_path=file_path)

        # self.add_docs(documents=documents)
        self.add_nodes(documents=documents)

        return documents

    def ingest_url(self, url: str) -> List[Document]:
        """Ingest content from a URL into the index."""

        documents = self.convert_url_to_docs(url)
        self.add_nodes(documents=documents)

        return documents

    def convert_file_to_docs(self, file_path: str) -> list[Document]:
        """Convert a file to documents."""
        file_path = Path(file_path)
        file_name = file_path.name
        custom_logger.debug(f"Converting {file_name} into documents")
        extension = file_path.suffix
        reader = self.default_file_reader_cls.get(extension)

        if reader is None:
            custom_logger.debug(
                f"No specific reader found for {extension}, using default string reader"
            )
            # Read as a plain text
            string_reader = StringIterableReader()
            documents = string_reader.load_data([file_path.read_text()])

        else:
            custom_logger.debug(f"Specific reader found for {extension}")
            documents = reader().load_data(file_path)

        for document in documents:
            document.metadata["doc_id"] = document.doc_id
            document.metadata["source"] = file_name
            document.text = self.ingest_helper.strip_consecutive_newlines(
                document.text
            ).strip()

        return documents

    def convert_url_to_docs(self, url: str) -> List[Document]:
        """Convert a url to documents."""

        loader = RemoteReader()
        documents = loader.load_data(url)

        return documents

    def get_or_create_index(self):
        """Get or create an index."""
        node_parser = SimpleNodeParser.from_defaults(
            chunk_size=1024,
            chunk_overlap=32,
        )

        embed_model = OpenAIEmbedding(api_key=config.OPENAI_API_KEY)

        transformations = [node_parser, embed_model]

        storage_context = StorageContext.from_defaults(
            docstore=self.doc_store,
            index_store=self.index_store,
            vector_store=self.vector_store,
        )

        existing_indexes = docs_execute.get_existing_indexes()
        if len(existing_indexes) > 0:
            index = load_index_from_storage(
                storage_context=storage_context,
                store_nodes_override=True,
                show_progress=True,
            )
            custom_logger.info(f"Loaded vector store index from storage")
            return index

        index = VectorStoreIndex.from_documents(
            documents=[],
            storage_context=storage_context,
            transformations=transformations,
            store_nodes_override=True,
            show_progress=True,
            index_id="mongo-index",
        )
        index.set_index_id("mongo-index")
        custom_logger.info(f"Created a new vector store index")
        return index

    def add_docs(self, documents: List[Document]) -> List[Document]:
        """Add documents to the index."""
        custom_logger.debug(f"Adding {len(documents)} documents into the index")
        for document in documents:
            self.index.insert(document, show_progress=True)

        custom_logger.debug(
            f"Succesfully added {len(documents)} documents into the index"
        )

        return documents

    def add_nodes(self, documents: List[Document]) -> List[BaseNode]:
        """Add nodes to the index."""
        parser = SentenceSplitter()
        nodes = parser.get_nodes_from_documents(documents, show_progress=True)

        # use multiple api keys to avoid rate limits and increase speed
        list_api_keys = config.OPENAI_API_KEY_EMBEDDINGS
        usage_counts = {key: 0 for key in list_api_keys}
        api_key_index = 0
        embed_model = OpenAIEmbedding(api_key=list_api_keys[api_key_index])

        for node in nodes:
            # if usage count is greater than 3, switch to the next api key
            if usage_counts[list_api_keys[api_key_index]] >= 3:
                api_key_index = (api_key_index + 1) % len(list_api_keys)
                usage_counts[list_api_keys[api_key_index]] = 0
                embed_model = OpenAIEmbedding(api_key=list_api_keys[api_key_index])

            node_embedding = embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
            usage_counts[list_api_keys[api_key_index]] += 1

        self.index.insert_nodes(nodes, show_progress=True)
        custom_logger.debug(nodes)

        return nodes

    def get_docs(self) -> List[TextNode]:
        """Get all documents."""
        documents = self.index.docstore.docs.values()

        return list(documents)

    @staticmethod
    def get_docs_by_file_name(file_name: str) -> List[TextNode]:
        """Get documents by file name."""
        documents = docs_execute.get_docs_by_file_name(file_name)

        return list(documents)

    def get_files(self) -> List[str]:
        """Get all files."""
        files = self.ingest_helper.get_all_files()

        return files

    def delete_docs_by_file_name(self, file_name: str):
        """Delete documents by file name."""
        docs_ids = docs_execute.get_docs_ids_by_file_name(file_name)
        for doc_id in docs_ids:
            self.index.delete_ref_doc(doc_id, delete_from_docstore=True)
        return docs_ids

    def delete_all_docs(self):
        """Delete all documents."""
        file_names = self.get_files()

        for file_name in file_names:
            self.delete_docs_by_file_name(file_name)
            self.ingest_helper.delete_file(file_name)

        return file_names


ingest_service = IngestService()
