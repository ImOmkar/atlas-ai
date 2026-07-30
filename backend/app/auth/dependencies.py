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


from collections.abc import Callable
from fastapi import Depends
from app.auth.enums import UserRole
from app.auth.exceptions import PermissionDeniedError


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


def require_roles(
    *roles: UserRole,
) -> Callable:
    def dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise PermissionDeniedError()

        return current_user

    return dependency