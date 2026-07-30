

class UserAlreadyExistsError(Exception):
    """Raised when a user tries to register with an existing email."""

class InvalidCredentialsError(Exception):
    """Raised when email or password is incorrect."""

class InvalidRefreshTokenError(Exception):
    """Raised when a refresh token is invalid."""