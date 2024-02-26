"""User model"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserBaseModel(BaseModel):
    """User base"""

    username: str
    password: str


class UserCreateModel(UserBaseModel):
    """User create"""


class UserModel(UserBaseModel):
    """User Schema"""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = datetime.now()
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "password": "password",
                "created_at": "2021-09-01T00:00:00",
            }
        },
    )


class UserCollectionModel(BaseModel):
    """User collection model"""

    users: List[UserModel]
