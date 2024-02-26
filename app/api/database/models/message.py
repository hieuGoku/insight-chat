"""Message model"""

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class MessageBaseModel(BaseModel):
    """Message base"""

    session_id: PyObjectId
    message: str
    sender: str


class MessageCreateModel(MessageBaseModel):
    """Create message model"""


class MessageModel(MessageBaseModel):
    """Message model"""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "5f8f1a6f4e3c4c8f0d4a8f6d",
                "session_id": "3f8f1a6f4e3c4c8f0d4a8f6d",
                "message": "Hello",
                "sender": "user",
                "created_at": "2020-10-20T14:00:00.000Z",
            }
        },
    )


class MessageCollectionModel(BaseModel):
    """Message collection model"""

    messages: List[MessageModel]
