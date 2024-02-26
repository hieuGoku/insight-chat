"""Chat model"""

from pydantic import BaseModel


class ChatBodyBaseModel(BaseModel):
    """Chat base"""

    session_id: str
    query: str


class ChatBodyModel(ChatBodyBaseModel):
    """Chat model"""

