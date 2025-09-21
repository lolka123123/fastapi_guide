import uuid

from passlib.context import CryptContext
import anyio
from fastapi import HTTPException, status
from datetime import timezone, datetime, timedelta
from jose import jwt, JWTError
from app.core.settings import settings
from typing import Tuple


pwd = CryptContext(schemes='bcrypt', deprecated="auto")

async def hash_password(password: str) -> str:
    return await anyio.to_thread.run_sync(pwd.hash, password)

async def verify_password(password: str, hashed: str) -> bool:
    return await anyio.to_thread. run_sync(pwd.verify, password, hashed)

UTS = timezone.utc

def time_now() -> datetime:
    return datetime.now(UTS)

def encode_token(payload: dict) -> str:
    return jwt.encode(claims=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def create_access_token(email: str) -> str:
    iat = time_now()
    exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)
    return encode_token({
        'sub': email,
        'type': 'access',
        'iat': int(iat.timestamp()),
        'exp': int(exp.timestamp())
    })

def create_refresh_token(email: str) -> Tuple[str, str, datetime]:
    iat = time_now()
    exp = iat + timedelta(minutes=settings.REFRESH_TOKEN_DAYS)
    jti = uuid.uuid4().hex
    token = encode_token({
        'sub': email,
        'type': 'refresh',
        'jti': jti,
        'iat': int(iat.timestamp()),
        'exp': int(exp.timestamp())
    })
    return token, jti, exp