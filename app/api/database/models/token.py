"""Token model."""

from typing import Optional
from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Token Schema."""

    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Token Payload."""

    sub: str = None
    exp: int = None


class TokenData(BaseModel):
    """Token Data."""

    username: Optional[str] = None
