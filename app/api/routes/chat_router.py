"""Chat router for the API."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.api.database.models.chat import ChatBodyModel
from app.api.services.session_service import SessionService
from app.api.services.chat_service import ChatService
from app.api.responses.base import BaseResponse
from app.logger.logger import custom_logger

router = APIRouter()

session_service = SessionService()
chat_service = ChatService()


@router.post("")
async def chat(chat_body: ChatBodyModel):
    """Chat with the document"""
    try:
        # session = session_service.get_session_by_id(chat_body.session_id)
        # if not session:
        #     return BaseResponse.error_response(
        #         status_code=404, message="Session not found"
        #     )
        return chat_service.query_en(chat_body.query, chat_body.session_id)
        # return StreamingResponse(
        #     chat_service.query(chat_body.query, chat_body.session_id),
        #     media_type="text/event-stream",
        # )


    except Exception as e:
        custom_logger.exception(e)
        return BaseResponse.error_response(
            status_code=400, message="Internal Server Error"
        )
