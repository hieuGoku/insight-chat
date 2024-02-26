"""User router for the API"""

from fastapi import APIRouter

from app.api.database.models.user import UserCreateModel, UserModel, UserCollectionModel
from app.api.services.user_service import UserService
from app.api.services.message_service import MessageService
from app.api.services.session_service import SessionService
from app.api.responses.base import BaseResponse
from app.logger.logger import custom_logger

router = APIRouter()

user_service = UserService()
message_service = MessageService()
session_service = SessionService()


@router.post("", response_model=UserModel, response_model_by_alias=False)
async def create_user(user: UserCreateModel):
    """Creates a new user."""
    try:
        return user_service.create_user(user)

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.get("", response_model=UserCollectionModel, response_model_by_alias=False)
async def get_users():
    """Get all users."""
    try:
        return user_service.get_users()

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.get("/{user_id}", response_model=UserModel, response_model_by_alias=False)
async def get_user(user_id: str):
    """Get user by ID."""
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            return BaseResponse.error_response(
                status_code=404, message="User not found"
            )

        return user

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")


@router.delete("/{user_id}", response_model=UserModel, response_model_by_alias=False)
async def delete_user(user_id: str):
    """Delete user by ID."""
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            return BaseResponse.error_response(
                status_code=404, message="User not found"
            )

        sessions_user = session_service.get_sessions_by_user_id(user_id)
        if sessions_user:
            for session in sessions_user.sessions:
                message_service.delete_messages_by_session_id(session.id)
                session_service.delete_session_by_id(session.id)

        user_service.delete_user_by_id(user_id)

        return BaseResponse.success_response(
            status_code=200, message="User deleted successfully", data=user_id
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(message="Internal Server Error")
