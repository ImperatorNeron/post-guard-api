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
from app.schemas.comments import ReadCommentSchema


if TYPE_CHECKING:
    from app.models.posts import Post
    from app.models.users import User


class Comment(
    IdIntPkMixin,
    UpdateCreateDateTimeMixin,
    BaseModel,
):
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
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def to_read_model(self):
        return ReadCommentSchema(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            content=self.content,
            is_blocked=self.is_blocked,
            blocked_reason=self.blocked_reason,
            user_id=self.user_id,
            post_id=self.post_id,
        )
