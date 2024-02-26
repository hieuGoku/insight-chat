"""Session router for the API."""

from fastapi import APIRouter

from app.api.database.models.session import SessionModel, SessionCreateModel
from app.api.services.session_service import SessionService
from app.api.services.user_service import UserService
from app.api.services.message_service import MessageService
from app.api.responses.base import BaseResponse
from app.api.errors.error_message import BaseErrorMessage
from app.logger.logger import custom_logger

router = APIRouter()

session_service = SessionService()
user_service = UserService()
message_service = MessageService()


@router.post("", response_model=SessionModel, response_model_by_alias=False)
async def create_session(session: SessionCreateModel):
    """Create chat session"""
    try:
        user = user_service.get_user_by_id(session.user_id)
        if not user:
            return BaseResponse.error_response(
                status_code=404, message="User not found"
            )

        return session_service.create_session(session)

    except ValueError as e:
        custom_logger.debug(str(e))
        error_message: BaseErrorMessage = e.args[0]
        return BaseResponse.error_response(
            status_code=400, message=error_message.message
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )


@router.get("/{session_id}", response_model=SessionModel, response_model_by_alias=False)
async def get_session(session_id: str):
    """Get chat session"""
    try:
        session = session_service.get_session_by_id(session_id)
        if not session:
            return BaseResponse.error_response(
                status_code=404, message="Session not found"
            )

        return session

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Delete chat session"""
    try:
        session = session_service.get_session_by_id(session_id)
        if not session:
            return BaseResponse.error_response(
                status_code=404, message="Session not found"
            )

        message_service.delete_messages_by_session_id(session_id)
        session_service.delete_session_by_id(session_id)

        return BaseResponse.success_response(
            status_code=200,
            message="Chat session deleted",
            data={"session_id": session_id},
        )

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )
