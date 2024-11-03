from typing import (
    Optional,
    TYPE_CHECKING,
)

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
    parent_comment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id"),
        nullable=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    parent_comment: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        remote_side="Comment.id",
        back_populates="replies",
    )
    replies: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent_comment",
        cascade="all, delete-orphan",
    )

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
            parent_comment_id=self.parent_comment_id,
        )
