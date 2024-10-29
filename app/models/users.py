from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import BaseModel
from app.models.mixins import (
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
)
from app.schemas.users import ReadUserWithPasswordSchema


if TYPE_CHECKING:
    from app.models.comments import Comment
    from app.models.posts import Post


class User(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
    )
    hashed_password: Mapped[bytes] = mapped_column(
        LargeBinary,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    is_auto_reply_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    auto_reply_delay: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
    )

    def to_read_model(self):
        return ReadUserWithPasswordSchema(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            email=self.email,
            username=self.username,
            is_verified=self.is_verified,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_auto_reply_enabled=self.is_auto_reply_enabled,
            auto_reply_delay=self.auto_reply_delay,
            hashed_password=self.hashed_password,
        )
