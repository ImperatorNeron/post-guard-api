from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class BaseCommentSchema(BaseModel):
    content: str = Field(title="Content of the comment")
    is_blocked: bool = Field(
        default=False,
        title="Indicates if the comment is blocked",
    )
    blocked_reason: Optional[str] = Field(
        default=None,
        max_length=255,
        title="Reason for blocking the comment",
    )


class ReadCommentSchema(BaseCommentSchema):
    id: PositiveInt = Field(title="Unique identifier")  # noqa
    user_id: PositiveInt = Field(
        title="ID of the user who made the comment",
    )
    post_id: PositiveInt = Field(
        title="ID of the post the comment is associated with",
    )
    created_at: datetime = Field(
        title="Timestamp when the comment was created",
    )
    updated_at: datetime = Field(
        title="Timestamp when the comment was last updated",
    )
