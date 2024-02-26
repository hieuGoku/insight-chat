"""Docs Execute module."""

from app.api.database.mongo_db import mongodb


class DocsExecute:
    """Docs execute for database operations."""

    @staticmethod
    def get_existing_indexes():
        return list(mongodb["index_store/data"].find())

    @staticmethod
    def get_docs_by_source(source: str):
        return list(mongodb["docstore/data"].find({"__data__.metadata.source": source}))

    @staticmethod
    def get_docs_ids_by_source(source: str):
        return list(
            mongodb["docstore/data"].distinct(
                "__data__.metadata.doc_id",
                {"__data__.metadata.source": source},
            )
        )

    @staticmethod
    def get_existing_sources():
        return list(
            mongodb["docstore/data"].distinct("__data__.metadata.source")
        )
