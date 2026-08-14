from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import RefreshToken, User
from app.auth.schemas import LoginRequest, LogoutRequest, PaginatedUsersResponse, RefreshRequest, SessionInfo, TokenResponse, UpdateUserRoleRequest, UpdateUserStatusRequest, UserCreate
from app.auth.security import create_access_token, generate_refresh_token, hash_password, hash_refresh_token, verify_password
from app.auth.user_repository import UserRepository
from app.auth.exceptions import InvalidCredentialsError, InvalidRefreshTokenError, UserAlreadyExistsError, UserNotFoundError

from datetime import UTC, datetime, timedelta

from app.auth.enums import UserRole
import math

class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)


    def get_all_users(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> PaginatedUsersResponse:

        users, total = self.user_repository.get_all_users(
            page=page,
            page_size=page_size,
            search=search,
            role=role,
            is_active=is_active,
        )

        return PaginatedUsersResponse(
            items=users,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size),
        )

    def register_user(
        self,
        user_data: UserCreate,
    ) -> User:

        existing_user = self.user_repository.get_by_email(user_data.email)

        if existing_user:
            raise UserAlreadyExistsError()

        hashed_password = hash_password(user_data.password)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=UserRole.USER,
        )

        return self.user_repository.create(user)
    

    def update_user_role(
        self,
        user_id: int,
        request: UpdateUserRoleRequest,
    ) -> User:

        user = self.user_repository.get_user_by_id(
            user_id,
        )

        if user is None:
            raise UserNotFoundError()

        user.role = request.role

        self.user_repository.save()

        return user

    def update_user_status(
        self,
        user_id: int,
        request: UpdateUserStatusRequest,
    ) -> User:

        user = self.user_repository.get_user_by_id(
            user_id,
        )

        if user is None:
            raise UserNotFoundError()

        user.is_active = request.is_active

        self.user_repository.save()

        return user
        
    def login(
        self,
        credentials: LoginRequest,
        session: SessionInfo,
    ) -> TokenResponse:
        # Find user by email
        user = self.user_repository.get_by_email(credentials.email)

        # User doesn't exist
        if user is None:
            raise InvalidCredentialsError()

        # User is inactive
        if not user.is_active:
            raise InvalidCredentialsError()

        # Password doesn't match
        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=str(user.id),
        )

        refresh_token = generate_refresh_token()

        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        expires_at = datetime.now(UTC) + timedelta(days=7)

        db_refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
        )

        self.user_repository.create_refresh_token(
            db_refresh_token,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def refresh_access_token(
        self,
        request: RefreshRequest,
        session: SessionInfo,
    ) -> TokenResponse:

        token_hash = hash_refresh_token(
            request.refresh_token
        )

        db_token = self.user_repository.get_refresh_token_by_hash(
            token_hash
        )

        if db_token is None:
            raise InvalidRefreshTokenError()

        if db_token.revoked_at is not None:
            raise InvalidRefreshTokenError()

        if db_token.expires_at < datetime.now(UTC):
            raise InvalidRefreshTokenError()


        user = db_token.user

        if not user.is_active:
            raise InvalidRefreshTokenError()

        access_token = create_access_token(
                    subject=str(user.id),
                )
        
        refresh_token = generate_refresh_token()

        refresh_token_hash = hash_refresh_token(
            refresh_token,
        )

        db_token.revoked_at = datetime.now(UTC)

        expires_at = datetime.now(UTC) + timedelta(days=7)
        
        db_refresh_token = RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
            expires_at=expires_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
        )

        self.user_repository.create_refresh_token(
            db_refresh_token,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    def logout(
        self,
        request: LogoutRequest,
    ) -> None:
        token_hash = hash_refresh_token(
            request.refresh_token,
        )

        db_token = self.user_repository.get_refresh_token_by_hash(
            token_hash,
        )

        if db_token is None:
            return

        if db_token.revoked_at is not None:
            return

        db_token.revoked_at = datetime.now(UTC)

        self.user_repository.save()
    