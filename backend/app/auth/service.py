from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserCreate
from app.auth.security import hash_password
from app.auth.user_repository import UserRepository


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register_user(
        self,
        user_data: UserCreate,
    ) -> User:

        existing_user = self.user_repository.get_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_password = hash_password(user_data.password)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
        )

        return self.user_repository.create(user)