from passlib.context import CryptContext
from datetime import timezone, datetime
from jose import jwt, JWTError
from app.core.settings import settings
#
# pwd_context = CryptContext(schemes='bcrypt', deprecated='auto')
#
# hashed_password = pwd_context.hash('test123')
# print(hashed_password)
#
# print(pwd_context.verify("test123", hashed_password))  # True
# print(pwd_context.verify("wrongpassword", hashed_password))     # False

# print(datetime.now(timezone.utc))

def encode_token(payload: dict) -> str:
    return jwt.encode(claims=payload, key=settings.SECRET_KEY, algorithm=[settings.ALGORITHM])



import uuid

from datetime import timezone, datetime, timedelta
from jose import jwt
from app.core.settings import settings
from typing import Tuple

UTS = timezone.utc

def time_now() -> datetime:
    return datetime.now(UTS)

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

print(create_refresh_token('khvan525@gmail.com'))