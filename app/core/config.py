import os
import json
from dotenv import load_dotenv
from app.logger.logger import custom_logger

load_dotenv()


class Config:
    """Config for the app."""

    # auth
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # local data
    LOCAL_DATA_FOLDER = os.getenv("LOCAL_DATA_FOLDER")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
    ALLOWED_EXTENSIONS = [
        "csv",
        "docx",
        "epub",
        "hwp",
        "ipynb",
        "jpeg",
        "jpg",
        "mbox",
        "md",
        "mp3",
        "mp4",
        "pdf",
        "png",
        "ppt",
        "pptm",
        "pptx",
    ]

    # qdrant
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")

    # docstore and indexstore
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    # openai api key for chat
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # openai api key for embedding
    OPENAI_API_KEY_EMBEDDINGS = (
        os.getenv("OPENAI_API_KEY_EMBEDDINGS", "").split(",")
    )

    # llm model
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

    # embedding model
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME")


def print_config(config: Config):
    """Print config."""
    custom_logger.debug("Printing config")
    for attr in dir(config):
        if attr.startswith("__"):
            continue
        print(f"  {attr}: {getattr(config, attr)}")


config = Config()
