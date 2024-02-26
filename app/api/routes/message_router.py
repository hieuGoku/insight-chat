"""Message router for the API."""

from fastapi import APIRouter

from app.api.database.models.message import (
    MessageModel,
    MessageCreateModel,
    MessageCollectionModel,
)
from app.api.services.message_service import MessageService
from app.api.services.session_service import SessionService
from app.api.responses.base import BaseResponse
from app.logger.logger import custom_logger

router = APIRouter()

message_service = MessageService()
session_service = SessionService()


@router.post("", response_model=MessageModel, response_model_by_alias=False)
async def create_message(message: MessageCreateModel):
    """Create a message"""
    try:
        session = session_service.get_session_by_id(message.session_id)
        if not session:
            return BaseResponse.error_response(
                status_code=404, message="Session not found"
            )

        return message_service.create_message(message)

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )


@router.get(
    "/{session_id}",
    response_model=MessageCollectionModel,
    response_model_by_alias=False,
)
async def get_messages_of_session(session_id: str):
    """Get chat session messages"""
    try:
        session = session_service.get_session_by_id(session_id)
        if not session:
            return BaseResponse.error_response(
                status_code=404, message="Session not found"
            )

        return message_service.get_messages_by_session_id(session_id)

    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )
