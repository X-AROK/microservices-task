from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import AuthError
from app.core.jwt import decode_token


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> int:
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise AuthError("Expired or invalid token")

    user_id = payload.get("user_id", None)
    if user_id is None:
        raise AuthError("Expired or invalid token")

    return user_id
