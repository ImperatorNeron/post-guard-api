from fastapi import (
    HTTPException,
    status,
)


class UserWasNotFoundError(HTTPException):
    def __init__(self, detail="User wasn`t found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class InactiveUserError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive.",
        )
