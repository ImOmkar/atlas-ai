from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import InvalidRefreshTokenError, UserAlreadyExistsError, InvalidCredentialsError

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(
        request: Request,
        exc: UserAlreadyExistsError,
    ):
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Email already registered"
            },
        )

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsError,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid email or password"
            },
        )

    @app.exception_handler(InvalidRefreshTokenError)
    async def invalid_refresh_token_handler(
        request: Request,
        exc: InvalidRefreshTokenError,
    ):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid refresh token"
            },
        )