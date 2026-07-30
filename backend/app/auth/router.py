from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import LogoutRequest, RefreshRequest, SessionInfo, UserCreate, UserResponse, TokenResponse, LoginRequest
from app.auth.service import AuthService
from app.db.dependencies import get_db

from app.auth.dependencies import get_current_user
from app.auth.models import User
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    return service.register_user(user_data)

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    credentials = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    session = SessionInfo(
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    return service.login(
        credentials=credentials,
        session=session,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def login(
    request: Request,
    refresh_request: RefreshRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    session = SessionInfo(
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )

    return service.refresh_access_token(
        request=refresh_request,
        session=session,
    )


@router.post(
    "/logout",
    status_code=204,
)
def logout(
    request: LogoutRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    service.logout(request)
    

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user
