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


class ModeratePostSchema(BasePostSchema):
    is_blocked: bool = Field(
        default=False,
        title="Indicates if the post is blocked",
    )
    blocked_reason: Optional[str] = Field(
        max_length=255,
        default=None,
        title="Reason for blocking the post",
    )


class ReadPostSchema(ModeratePostSchema):
    id: PositiveInt = Field(title="Unique identifier")  # noqa
    user_id: PositiveInt = Field(
        title="ID of the user who made the post",
    )
    created_at: datetime = Field(
        title="Timestamp when the post was created",
    )
    updated_at: datetime = Field(
        title="Timestamp when the post was last updated",
    )
