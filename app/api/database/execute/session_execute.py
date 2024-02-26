"""Session Execute module."""

from bson import ObjectId

from app.api.database.mongo_db import mongodb
from app.api.database.models.session import SessionModel


class SessionExecute:
    """Session execute for database operations."""

    @staticmethod
    def create_session(session: SessionModel):
        new_session = mongodb["sessions"].insert_one(
            session.model_dump(by_alias=True, exclude=["id"])
        )
        created_session = mongodb["sessions"].find_one(
            {"_id": new_session.inserted_id}
        )

        return created_session

    @staticmethod
    def get_session_by_id(session_id: str):
        return mongodb["sessions"].find_one({"_id": ObjectId(session_id)})

    @staticmethod
    def get_sessions_by_user_id(user_id: str):
        return list(mongodb["sessions"].find({"user_id": user_id}))

    @staticmethod
    def delete_session_by_id(session_id: str):
        mongodb["sessions"].delete_one({"_id": ObjectId(session_id)})
        return session_id
