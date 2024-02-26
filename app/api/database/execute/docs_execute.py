"""Docs Execute module."""

from app.api.database.mongo_db import mongodb_client


class DocsExecute:
    """Docs execute for database operations."""
    
    @staticmethod
    def get_existing_indexes():
        return list(mongodb_client["index_store/data"].find())

    @staticmethod
    def get_docs_by_file_name(file_name: str):
        return list(
            mongodb_client["docstore/data"].find(
                {"__data__.metadata.file_name": file_name}
            )
        )

    @staticmethod
    def get_docs_ids_by_file_name(file_name: str):
        return list(
            mongodb_client["docstore/data"].distinct(
                "__data__.metadata.doc_id",
                {"__data__.metadata.file_name": file_name},
            )
        )
