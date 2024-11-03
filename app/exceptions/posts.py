from fastapi import (
    HTTPException,
    status,
)


class PostNotFoundError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found or you do not have access.",
        )


class PostBlockedError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post with id {post_id} is blocked and cannot be read or changed.",
        )
