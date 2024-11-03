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


class CommentNotFoundError(HTTPException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found or you do not have access.",
        )


class CommentBlockedError(HTTPException):
    def __init__(self, comment_id: int):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Comment with id {comment_id} is blocked and cannot be changed.",
        )
