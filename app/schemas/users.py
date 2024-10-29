from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PositiveInt,
)


class BaseUserSchema(BaseModel):
    email: EmailStr = Field(
        max_length=255,
        title="Email address of the user",
    )
    username: str = Field(
        max_length=50,
        title="Username of the user",
    )


class ReadUserSchema(BaseUserSchema):
    id: PositiveInt  # noqa
    is_active: bool = Field(
        default=True,
        title="Indicates if the user is active",
    )
    is_superuser: bool = Field(
        default=False,
        title="Indicates if the user is a superuser",
    )
    is_verified: bool = Field(
        default=False,
        title="Indicates if the user is verified",
    )
    created_at: datetime = Field(
        title="Timestamp when the post was created",
    )
    updated_at: datetime = Field(
        title="Timestamp when the post was last updated",
    )
    is_auto_reply_enabled: bool = Field(
        default=False,
        title="Indicates if auto-reply is enabled",
    )
    auto_reply_delay: PositiveInt = Field(
        default=60,
        title="Delay for auto-replies in seconds",
    )


class ReadUserWithPasswordSchema(ReadUserSchema):
    hashed_password: bytes


class RegisterUserSchema(BaseUserSchema):
    password: str


class CreateUserSchema(BaseUserSchema):
    hashed_password: bytes


class LoginUserSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str = Field(max_length=255)
