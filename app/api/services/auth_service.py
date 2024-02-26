"""Authentication service module."""

from typing import Optional, Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

from app.api.database.models.user import UserModel
from app.api.database.execute.user_execute import UserExecute
from app.api.database.models.auth import oauth2_scheme, pwd_context
from app.core.config import config

user_execute = UserExecute()


def get_hashed_password(password: str) -> str:
    """Hash password."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    """Verify password."""
    return pwd_context.verify(password, hashed_pass)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


def authenticate_user(username: str, password: str) -> bool | UserModel:
    """Authenticate user."""
    user = user_execute.get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Check login token of current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        print(f"usernameee: {username}")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = user_execute.get_user_by_username(username=username)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    """Get current active user."""
    return current_user
