from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import bcrypt
from jwt import decode, encode

from src.utils.settings import Settings

settings = Settings()


def create_access_token(payload: dict):
    access_token = encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return access_token


def create_refresh_token(access_token: str):
    refresh_token = bcrypt.hashpw(
        access_token.encode('utf8'), bcrypt.gensalt(12)
    ).decode('utf8')
    return refresh_token


def verify_refresh_token(access_token: str, refresh_token: str):
    return bcrypt.checkpw(
        access_token.encode('utf8'), refresh_token.encode('utf8')
    )


def update_exp_access_token(access_token: str):
    payload = decode(
        access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
        options={'verify_exp': False},
    )
    payload['exp'] = datetime.now(ZoneInfo(settings.TZ)) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return create_access_token(payload)
