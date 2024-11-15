# TODO: Изменить метод шифрованя на ассметрчный для большей безопасности

from datetime import datetime, timedelta

import jwt

from app.core.config import config

ALGORITHM = "HS256"


def create_token(payload: dict) -> str:
    exp = datetime.now() + timedelta(minutes=config.TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"exp": exp, **payload}, config.SECRET_KEY, algorithm=ALGORITHM)

    return token


def decode_token(token: str) -> dict | None:
    try:
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        exp = datetime.fromtimestamp(decoded["exp"])
        if exp < datetime.now():
            return None
        return decoded
    except Exception:
        return None
