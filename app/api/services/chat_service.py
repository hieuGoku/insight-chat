"""Chat service module."""

from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.base.llms.types import ChatMessage, MessageRole

from app.api.database.models.message import MessageCreateModel
from app.api.services.message_service import MessageService
from app.api.services.ingest_service import ingest_service
import llama_index.core

llama_index.core.set_global_handler("simple")


class ChatService:
    """Chat Service class for chat operations."""

    def __init__(self):
        self.message_service = MessageService()

    @staticmethod
    def chat(query: str):
        """Chat with the document."""

        chat_engine = ingest_service.index.as_query_engine(
            similarity_top_k=5, streaming=True, verbose=False
        )
        streaming_response = chat_engine.query(query)

        return streaming_response.response_gen

    def conversation(self, query: str, session_id: str):
        """Get answer from the chat engine."""

        history = self.message_service.get_messages_by_session_id(session_id)
        chat_history = []
        if history.messages:
            for message in history.messages:
                chat_history.append(
                    ChatMessage(
                        message=message.message,
                        role=(
                            MessageRole.USER
                            if message.sender == "user"
                            else MessageRole.ASSISTANT
                        ),
                    )
                )

        memory = ChatMemoryBuffer.from_defaults(
            chat_history=chat_history, token_limit=8000
        )
        chat_engine = ingest_service.index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            similarity_top_k=5,
            verbose=False,
            system_prompt=(
                """\
            You are a chatbot. You MUST NOT provide any information unless it is in the Context or previous messages or general conversation. If the user ask something you don't know, say that you cannot answer. \
            you MUST keep the answers short and simple. \
            """
            ),
        )

        response = chat_engine.stream_chat(message=query)

        for token in response.response_gen:
            yield token

        self.message_service.create_message(
            message=MessageCreateModel(
                session_id=session_id,
                message=query,
                sender="user",
            )
        )
        self.message_service.create_message(
            message=MessageCreateModel(
                session_id=session_id,
                message=str(response),
                sender="assistant",
            )
        )
