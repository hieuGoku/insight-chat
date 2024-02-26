"""User Execute module."""

from bson import ObjectId

from app.api.database.mongo_db import mongodb
from app.api.database.models.user import UserModel


class UserExecute:
    """User execute for database operations."""

    @staticmethod
    def create_user(user: UserModel):
        return mongodb["users"].insert_one(
            user.model_dump(by_alias=True, exclude=["id"])
        )

    @staticmethod
    def get_users():
        return list(mongodb["users"].find())

    @staticmethod
    def get_user_by_id(user_id: str | ObjectId):
        return mongodb["users"].find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_user_by_username(username: str):
        return mongodb["users"].find_one({"username": username})

    @staticmethod
    def delete_user_by_id(user_id: str):
        mongodb["users"].delete_one({"_id": ObjectId(user_id)})
        return user_id
