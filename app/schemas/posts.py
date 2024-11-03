from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class BasePostSchema(BaseModel):
    title: str = Field(max_length=150, title="Title of the post")
    content: str = Field(title="Content of the post")


class CreatePostSchema(BasePostSchema):
    pass


class CreatePostWithUserSchema(BasePostSchema):
    user_id: PositiveInt = Field(
        title="ID of the user who made the post",
    )


class UpdatePostSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class ModeratePostSchema(BasePostSchema):
    user_id: PositiveInt = Field(
        title="ID of the user who made the post",
    )
    is_blocked: bool = Field(
        default=False,
        title="Indicates if the post is blocked",
    )
    blocked_reason: Optional[str] = Field(
        max_length=255,
        default=None,
        title="Reason for blocking the post",
    )


class UpdateModeratePostSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None


class ReadPostSchema(ModeratePostSchema):
    id: PositiveInt = Field(title="Unique identifier")  # noqa
    created_at: datetime = Field(
        title="Timestamp when the post was created",
    )
    updated_at: datetime = Field(
        title="Timestamp when the post was last updated",
    )
