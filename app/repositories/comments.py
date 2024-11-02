from datetime import datetime
from typing import Optional

from sqlalchemy import (
    func,
    select,
)

from app.models.comments import Comment
from app.models.posts import Post
from app.schemas.analytics import CommentAnalyticSchema
from app.utils.sql_repository import SQLAlchemyRepository


class CommentRepository(SQLAlchemyRepository):

    model = Comment

    async def get_comments_daily_breakdown(
        self,
        date_from: datetime,
        date_to: datetime,
        user_id: Optional[int] = None,
    ):
        stmt = (
            select(
                func.date(self.model.created_at).label("date"),
                func.count(self.model.id)
                .filter(self.model.is_blocked == False)  # noqa
                .label("created_count"),
                func.count(self.model.id)
                .filter(self.model.is_blocked == True)  # noqa
                .label("blocked_count"),
            )
            .join(Post, self.model.post_id == Post.id)
            .where(
                self.model.created_at >= date_from,
                self.model.created_at <= date_to,
            )
        )

        if user_id is not None:
            stmt = stmt.where(Post.user_id == user_id)

        stmt = stmt.group_by(func.date(self.model.created_at)).order_by(
            func.date(self.model.created_at),
        )

        results = await self.session.execute(stmt)
        return [
            CommentAnalyticSchema(
                date=str(result.date),
                created_count=result.created_count,
                blocked_count=result.blocked_count,
            )
            for result in results
        ]
