"""Vector database client."""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import CollectionDescription

from app.core.config import config
from app.logger.logger import custom_logger

custom_logger.info("Initializing vector database client")
vector_db_client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
)


def get_or_create_collection(collection_name: str):
    """
    The function `get_or_create_collection` checks if a collection with a given name exists in a Qdrant
    DB, and if not, creates it.

    :param collection_name: The `collection_name` parameter is a string that represents the name of the
    collection you want to get or create in the Qdrant DB
    :type collection_name: str
    :return: The function `get_or_create_collection` returns the name of the collection, which is
    `collection_name`.
    """
    collection_description = CollectionDescription(name=collection_name)
    list_of_collections = vector_db_client.get_collections().collections

    if collection_description in list_of_collections:
        custom_logger.info(
            f"Found collection {collection_name} in Qdrant DB, skipping creation and using it."
        )
        return collection_name

    custom_logger.info(f"Creating collection {collection_name} in Qdrant DB")
    vector_db_client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )
    return collection_name


get_or_create_collection(config.COLLECTION_NAME)
