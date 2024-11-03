from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
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
from app.schemas.posts import ReadPostSchema


if TYPE_CHECKING:
    from app.models.comments import Comment
    from app.models.users import User


class Post(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):
    title: Mapped[str] = mapped_column(String(150))
    content: Mapped[str] = mapped_column(Text)
    is_blocked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
    )
    blocked_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        cascade="all, delete",
        back_populates="post",
    )

    def to_read_model(self):
        return ReadPostSchema(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            title=self.title,
            content=self.content,
            is_blocked=self.is_blocked,
            blocked_reason=self.blocked_reason,
            user_id=self.user_id,
        )
