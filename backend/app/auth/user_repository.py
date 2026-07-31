from sqlalchemy.orm import Session
from app.auth.models import RefreshToken
from app.auth.models import User
from sqlalchemy import or_

from app.auth.enums import UserRole

class UserRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )


    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    
    def get_by_id(
        self,
        user_id: int,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )


    def get_all_users(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        
        query = self.db.query(User)

        if search:
            query = query.filter(
                or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )

        if role is not None:
            query = query.filter(
                User.role == role,
            )

        if is_active is not None:
            query = query.filter(
                User.is_active == is_active,
            )

        total = query.count()

        users = (
            query
            .order_by(User.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return users, total


    def create_refresh_token(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_refresh_token_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token_hash == token_hash
            )
            .first()
        )

    def save(self):
        self.db.commit()