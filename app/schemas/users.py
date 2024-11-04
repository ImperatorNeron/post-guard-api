from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PositiveInt,
)


class BaseUserSchema(BaseModel):
    email: EmailStr = Field(max_length=255, title="Email address of the user")
    username: str = Field(min_length=3, max_length=50, title="Username of the user")


class ReadUserSchema(BaseUserSchema):
    id: PositiveInt  # noqa
    is_active: bool = Field(default=True, title="Indicates if the user is active")
    is_superuser: bool = Field(
        default=False,
        title="Indicates if the user is a superuser",
    )
    is_verified: bool = Field(default=False, title="Indicates if the user is verified")
    created_at: datetime = Field(None, title="Timestamp when the post was created")
    updated_at: datetime = Field(None, title="Timestamp when the post was last updated")
    is_auto_reply_enabled: bool = Field(
        default=False,
        title="Indicates if auto-reply is enabled",
    )
    auto_reply_delay: PositiveInt = Field(
        default=60,
        title="Delay for auto-replies in seconds",
    )


class RegisterUserSchema(BaseUserSchema):
    password: str = Field(
        min_length=4,
        max_length=255,
        title="User's password for registration",
    )


class ReadUserWithPasswordSchema(ReadUserSchema):
    hashed_password: bytes = Field(title="Hashed user's password")


class CreateUserSchema(BaseUserSchema):
    hashed_password: bytes = Field(title="Hashed user's password")


class UpdateUserSchema(BaseModel):
    is_auto_reply_enabled: Optional[bool] = Field(
        None,
        title="Enable or disable auto-reply",
    )
    auto_reply_delay: Optional[PositiveInt] = Field(
        None,
        title="Auto-reply delay in seconds",
    )


class LoginUserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50, title="Username for login")
    password: str = Field(min_length=4, max_length=255, title="Password for login")
