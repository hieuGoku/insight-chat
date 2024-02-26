"""User service module."""

from app.api.database.models.user import UserModel, UserCreateModel, UserCollectionModel
from app.api.database.execute.user_execute import UserExecute
from app.api.database.execute.session_execute import SessionExecute
from app.api.database.execute.message_execute import MessageExecute
from app.api.services import auth_service

user_execute = UserExecute()
session_execute = SessionExecute()
message_execute = MessageExecute()


class UserService:
    """User Service class for user operations."""

    @staticmethod
    def create_user(user: UserCreateModel):
        """Create a new user."""

        user_data = UserModel(username=user.username, password=user.password)
        user_data.password = auth_service.get_hashed_password(user_data.password)
        new_user = user_execute.create_user(user_data)
        created_user = user_execute.get_user_by_id(new_user.inserted_id)

        return UserModel(**created_user)

    @staticmethod
    def get_users():
        """Get all users."""

        users = user_execute.get_users()

        return UserCollectionModel(users=users)

    @staticmethod
    def get_user_by_id(user_id: str):
        """Get user by ID."""

        user = user_execute.get_user_by_id(user_id)
        if user:
            return UserModel(**user)

    @staticmethod
    def get_user_by_username(username: str):
        """Get user by username."""

        user = user_execute.get_user_by_username(username)
        if user:
            return UserModel(**user)

    @staticmethod
    def delete_user_by_id(user_id: str):
        """Delete user by ID."""

        return user_execute.delete_user_by_id(user_id)
