from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import RefreshToken, User
from app.auth.schemas import LoginRequest, LogoutRequest, RefreshRequest, SessionInfo, TokenResponse, UserCreate
from app.auth.security import create_access_token, generate_refresh_token, hash_password, hash_refresh_token, verify_password
from app.auth.user_repository import UserRepository
from app.auth.exceptions import InvalidCredentialsError, InvalidRefreshTokenError, UserAlreadyExistsError

from datetime import UTC, datetime, timedelta


class AuthService:

    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

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
        )

        return self.user_repository.create(user)

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
