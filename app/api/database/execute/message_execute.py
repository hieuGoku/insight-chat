"""Message Execute module."""

from app.api.database.mongo_db import mongodb
from app.api.database.models.message import MessageModel


class MessageExecute:
    """Message execute for database operations."""

    @staticmethod
    def create_message(message: MessageModel):
        new_message = mongodb["messages"].insert_one(
            message.model_dump(by_alias=True, exclude=["id"])
        )
        created_message = mongodb["messages"].find_one({"_id": new_message.inserted_id})

        return created_message

    @staticmethod
    def get_messages_by_session_id(session_id: str):
        return list(
            mongodb["messages"]
            .find({"session_id": session_id})
            .sort("created_at", -1)
            .limit(4)
        )

    @staticmethod
    def delete_messages_by_session_id(session_id: str):
        return mongodb["messages"].delete_many({"session_id": session_id}).deleted_count
