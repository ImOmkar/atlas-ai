from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.auth.exceptions import InvalidRefreshTokenError, PermissionDeniedError, UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError
from app.organizations.exceptions import OrganizationMemberNotFoundError, OrganizationNotFoundError
from app.projects.exceptions import ProjectNotFoundError
from app.documents.exceptions import DocumentFileNotFoundError, DocumentNotFoundError
from app.proposals.exceptions import ProposalProcessingError

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

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_exception_handler(
        request: Request,
        exc: PermissionDeniedError,
    ):
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Permission denied",
            },
        )

    @app.exception_handler(UserNotFoundError)
    async def user_not_found_exception_handler(
        request: Request,
        exc: UserNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "User not found",
            },
        )

    @app.exception_handler(OrganizationNotFoundError)
    async def organization_not_found_exception_handler(
        request: Request,
        exc: OrganizationNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Organization not found",
            },
        )

    @app.exception_handler(OrganizationMemberNotFoundError)
    async def organization_member_not_found_exception_handler(
        request: Request,
        exc: OrganizationMemberNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Organization member not found",
            },
        )


    @app.exception_handler(ProjectNotFoundError)
    async def project_not_found_exception_handler(
        request: Request,
        exc: ProjectNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Project not found",
            },
        )


    @app.exception_handler(DocumentNotFoundError)
    async def document_not_found_exception_handler(
        request: Request,
        exc: DocumentNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Document not found",
            },
        )


    @app.exception_handler(DocumentFileNotFoundError)
    async def document_file_not_found_exception_handler(
        request: Request,
        exc: DocumentFileNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Document file not found",
            },
        )


    @app.exception_handler(ProposalProcessingError)
    async def no_document_chunks_found_exception_handler(
        request: Request,
        exc: ProposalProcessingError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": "No document chunks found",
            },
        )