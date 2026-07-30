from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError
from app.core.config import settings
from app.auth.exceptions import InvalidCredentialsError
import secrets
import hashlib

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )

def create_access_token(
    subject: str,
) -> str:
    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except InvalidTokenError:
        raise InvalidCredentialsError()


def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure refresh token.
    """
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    """
    Hash a refresh token before storing it.
    """
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def verify_refresh_token(
    token: str,
    token_hash: str,
) -> bool:
    return hash_refresh_token(token) == token_hash