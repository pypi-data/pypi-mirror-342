from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from ...core.config import settings
from ...dependencies import auth, current_user_dependency
from ..schemas.auth import Token, User

router = APIRouter(tags=["Authentication"])


@router.post("/connect")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/refresh")
def refresh_token(current_user: Annotated[User, current_user_dependency]):
    new_access_token = auth.create_access_token(
        data={"sub": current_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": new_access_token}
