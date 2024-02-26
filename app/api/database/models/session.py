"""Session model"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class SessionBaseModel(BaseModel):
    """Chat session base"""

    user_id: PyObjectId


class SessionCreateModel(SessionBaseModel):
    """Chat session create"""


class SessionModel(SessionBaseModel):
    """Chat session schema"""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "1234567890",
                "user_id": "1234567890",
                "created_at": "2021-09-01T00:00:00",
            }
        },
    )


class SessionCollectionModel(BaseModel):
    """Chat session collection"""

    sessions: List[SessionModel]

