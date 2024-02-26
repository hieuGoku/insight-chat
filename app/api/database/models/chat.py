"""Chat model"""

from pydantic import BaseModel


class ChatBodyBaseModel(BaseModel):
    """Chat base"""

    query: str


class ChatBodyModel(ChatBodyBaseModel):
    """Chat model"""


class ConversationBodyModel(ChatBodyBaseModel):
    """Conversation model"""

    session_id: str

