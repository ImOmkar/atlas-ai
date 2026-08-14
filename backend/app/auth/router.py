from fastapi import Query, Request, APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.schemas import LogoutRequest, PaginatedUsersResponse, RefreshRequest, SessionInfo, UpdateUserRoleRequest, UpdateUserStatusRequest, UserCreate, UserListResponse, UserResponse, TokenResponse, LoginRequest
from app.auth.service import AuthService
from app.db.dependencies import get_db

from app.auth.dependencies import get_current_user, require_roles
from app.auth.models import User
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.enums import UserRole


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


@router.get("/admin")
def admin_only(
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
        )
    ),
):
    return {
        "message": "Welcome Admin",
    }



@router.get(
    "/users",
    response_model=PaginatedUsersResponse,
)
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(default=None),
    role: UserRole | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.get_all_users(
        page=page,
        page_size=page_size,
        search=search,
        role=role,
        is_active=is_active,
    )


@router.patch(
    "/users/{user_id}/role",
    response_model=UserResponse,
)
def update_user_role(
    user_id: int,
    request: UpdateUserRoleRequest,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.update_user_role(
        user_id=user_id,
        request=request,
    )

@router.patch(
    "/users/{user_id}/status",
    response_model=UserResponse,
)
def update_user_status(
    user_id: int,
    request: UpdateUserStatusRequest,
    current_user: User = Depends(
        require_roles(UserRole.ADMIN),
    ),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    return service.update_user_status(
        user_id=user_id,
        request=request,
    )