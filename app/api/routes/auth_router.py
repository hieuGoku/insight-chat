"""Authentication router for the API."""

import base64
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import RedirectResponse

from app.api.database.models.token import TokenSchema
from app.api.database.models.user import UserModel
from app.api.database.models.auth import basic_auth, BasicAuth
from app.api.services import auth_service
from app.core.config import config


router = APIRouter()


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login token."""
    user = auth_service.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/login")
async def login_basic(auth: BasicAuth = Depends(basic_auth)):
    """Login and get token."""
    if not auth:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)

    try:
        decoded = base64.b64decode(auth).decode("ascii")
        username, _, password = decoded.partition(":")
        user = auth_service.authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )

        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        token = jsonable_encoder(access_token)

        response = RedirectResponse(url="/docs")
        response.set_cookie(
            "Authorization",
            value=f"Bearer {token}",
            httponly=True,
            max_age=1800,
            expires=1800,
        )
        return response

    except HTTPException:
        return Response(headers={"WWW-Authenticate": "Basic"}, status_code=401)


@router.get("/logout")
async def route_logout_and_remove_cookie():
    """Logout and remove cookie."""
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization")
    return response


@router.get("/docs")
async def get_documentation():
    """Get documentation."""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@router.get("/me", response_model=UserModel, response_model_by_alias=False)
async def read_user_me(
    current_user: Annotated[
        UserModel, Depends(auth_service.get_current_active_user)
    ]
):
    """Get information of current user."""

    return current_user
