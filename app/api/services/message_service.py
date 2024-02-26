"""Message service module."""

from app.api.database.execute.message_execute import MessageExecute
from app.api.database.models.message import (
    MessageModel,
    MessageCreateModel,
    MessageCollectionModel,
)

message_execute = MessageExecute()


class MessageService:
    """Message Service class for message operations."""

    @staticmethod
    def create_message(message: MessageCreateModel):
        """Create a new message."""

        new_message = MessageModel(
            session_id=message.session_id,
            message=message.message,
            sender=message.sender,
        )
        created_message = message_execute.create_message(new_message)

        return MessageModel(**created_message)

    @staticmethod
    def get_messages_by_session_id(session_id: str):
        """Get chat session messages"""

        messages = message_execute.get_messages_by_session_id(session_id)

        return MessageCollectionModel(messages=messages)

    @staticmethod
    def delete_messages_by_session_id(session_id: str):
        """Delete chat session messages"""

        return message_execute.delete_messages_by_session_id(session_id)
