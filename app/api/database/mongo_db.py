"""MongoDB database client."""

import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore

from app.core.config import config
from app.logger.logger import custom_logger

mongodb_client = pymongo.MongoClient(config.MONGO_URI)
mongodb = mongodb_client.get_database(config.MONGO_DB_NAME)
custom_logger.info("Connected to MongoDB Atlas")

vector_store = MongoDBAtlasVectorSearch(
    mongodb_client=mongodb_client,
    db_name=config.MONGO_DB_NAME,
    collection_name="vector_store",
    index_name="vector_index",
)
custom_logger.info("Connected to MongoDB Atlas Vector Store")

index_store = MongoIndexStore.from_uri(config.MONGO_URI, db_name=config.MONGO_DB_NAME)
custom_logger.info("Connected to MongoDB Atlas Index Store")

doc_store = MongoDocumentStore.from_uri(config.MONGO_URI, db_name=config.MONGO_DB_NAME)
custom_logger.info("Connected to MongoDB Atlas Document Store")
