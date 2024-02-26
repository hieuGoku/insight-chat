"""Session service module."""

from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.memory import ChatMemoryBuffer

from app.api.database.execute.session_execute import SessionExecute
from app.api.database.models.session import (
    SessionModel,
    SessionCreateModel,
    SessionCollectionModel,
)
from app.api.services.message_service import MessageService
from app.api.services.ingest_service import ingest_service
from app.api.errors.error_message import SessionNotFoundError

session_execute = SessionExecute()
message_service = MessageService()


class SessionService:
    """Session Service class for session operations."""

    def query(self, query: str, chat_session_id: str):
        history = self.get_chat_session_messages(chat_session_id)
        chat_history = []
        for message in history:
            print(message)
            chat_history.append(
                ChatMessage(
                    role=(
                        MessageRole.USER
                        if message.sender == "user"
                        else MessageRole.ASSISTANT
                    ),
                    content=message.message,
                )
            )
        memory = ChatMemoryBuffer.from_defaults(chat_history=chat_history)
        chat_engine = ingest_service.index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            verbose=True,
        )

        response = chat_engine.chat(message=query)

        session_execute.create_message(
            chat_session_id=chat_session_id, message=query, sender="user"
        )
        session_execute.create_message(
            chat_session_id=chat_session_id,
            message=str(response),
            sender="assistant",
        )

        return response

        # for token in response.response_gen:
        #     yield token

    @staticmethod
    def create_session(session: SessionCreateModel):
        """Create a new chat session."""

        new_session = SessionModel(user_id=session.user_id)
        created_session = session_execute.create_session(new_session)

        return SessionModel(**created_session)

    @staticmethod
    def get_session_by_id(session_id: str):
        """Get chat session by id."""

        session = session_execute.get_session_by_id(session_id)
        if session:
            return SessionModel(**session)

    @staticmethod
    def get_sessions_by_user_id(user_id: str):
        """Get chat sessions by user id."""

        sessions = session_execute.get_sessions_by_user_id(user_id)
        if sessions:
            return SessionCollectionModel(sessions=sessions)

    @staticmethod
    def delete_session_by_id(session_id: str):
        """Delete chat session by id."""

        return session_execute.delete_session_by_id(session_id)
