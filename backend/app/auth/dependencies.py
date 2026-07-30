from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends

from sqlalchemy.orm import Session

from app.auth.security import (
    decode_access_token,
)

from app.auth.user_repository import UserRepository

from app.db.dependencies import get_db

from app.auth.exceptions import InvalidCredentialsError

from app.auth.models import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidCredentialsError()

    repository = UserRepository(db)

    user = repository.get_by_id(int(user_id))

    if user is None:
        raise InvalidCredentialsError()

    return user
