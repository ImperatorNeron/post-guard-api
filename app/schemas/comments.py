from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class BaseCommentSchema(BaseModel):
    content: str = Field(
        min_length=1,
        title="Content of the comment",
        description="The main content of the user's comment.",
    )


class CreateCommentSchema(BaseCommentSchema):
    parent_comment_id: Optional[PositiveInt] = Field(
        None,
        title="ID of the parent comment, if this is a reply",
    )


class UpdateCommentSchema(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=1,
        title="Updated content of the comment",
    )


class UpdateModerateCommentSchema(BaseModel):
    content: Optional[str] = Field(
        None,
        min_length=1,
        title="Updated content of the comment",
    )
    is_blocked: Optional[bool] = Field(
        None,
        title="Indicates if the comment is blocked",
    )
    blocked_reason: Optional[str] = Field(
        None,
        max_length=255,
        title="Reason for blocking the comment",
        description="Explanation for why the comment was blocked, if applicable.",
    )


class CreateCommentByPostSchema(CreateCommentSchema):
    user_id: PositiveInt = Field(title="ID of the user who made the comment")
    post_id: PositiveInt = Field(title="ID of the post the comment is associated with")


class ModerateCommentSchema(CreateCommentByPostSchema):
    is_blocked: bool = Field(
        default=False,
        title="Indicates if the comment is blocked",
    )
    blocked_reason: Optional[str] = Field(
        default=None,
        max_length=255,
        title="Reason for blocking the comment",
        description="Explanation for blocking the comment, if applicable.",
    )


class ReadCommentSchema(ModerateCommentSchema):
    id: PositiveInt = Field(title="Unique identifier")  # noqa
    created_at: Optional[datetime] = Field(
        None,
        title="Timestamp when the comment was created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Timestamp when the comment was last updated",
    )
