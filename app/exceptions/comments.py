from fastapi import (
    HTTPException,
    status,
)


class CommentBlockedPostError(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post with id {post_id} is blocked and cannot be commented.",
        )
