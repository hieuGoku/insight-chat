"""MongoDB database client."""

import pymongo

from app.core.config import config

mongodb_client = pymongo.MongoClient(config.MONGO_URI).get_database(
    config.MONGO_DB_NAME
)