from fastapi import (
    HTTPException,
    status,
)


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )


class InvalidJWTTokenError(HTTPException):
    def __init__(self, error_detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {error_detail}",
        )
