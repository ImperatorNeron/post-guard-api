from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class BasePostSchema(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=150,
        title="Title of the post",
        description="A brief, descriptive title.",
    )
    content: str = Field(
        min_length=10,
        title="Content of the post",
        description="Detailed content of the post.",
    )


class CreatePostSchema(BasePostSchema):
    pass


class CreatePostWithUserSchema(BasePostSchema):
    user_id: PositiveInt = Field(
        title="ID of the user who made the post",
    )


class UpdatePostSchema(BaseModel):
    title: Optional[str] = Field(
        None,
        min_length=5,
        max_length=150,
        title="Updated title of the post",
    )
    content: Optional[str] = Field(
        None,
        min_length=10,
        title="Updated content of the post",
    )


class ModeratePostSchema(CreatePostWithUserSchema):
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
    title: Optional[str] = Field(
        None,
        min_length=5,
        max_length=150,
        title="Updated title of the post",
    )
    content: Optional[str] = Field(
        None,
        min_length=10,
        title="Updated content of the post",
    )
    is_blocked: Optional[bool] = Field(
        None,
        title="Indicates if the post is blocked",
    )
    blocked_reason: Optional[str] = Field(
        None,
        max_length=255,
        title="Reason for blocking the post",
    )


class ReadPostSchema(ModeratePostSchema):
    id: PositiveInt = Field(title="Unique identifier")  # noqa
    created_at: Optional[datetime] = Field(
        None,
        title="Timestamp when the post was created",
    )
    updated_at: Optional[datetime] = Field(
        None,
        title="Timestamp when the post was last updated",
    )
