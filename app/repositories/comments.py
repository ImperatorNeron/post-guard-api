from datetime import datetime
from typing import Optional

from sqlalchemy import (
    case,
    func,
    select,
)

from app.models.comments import Comment
from app.models.posts import Post
from app.schemas.analytics import CommentAnalyticSchema
from app.utils.sql_repository import SQLAlchemyRepository


class CommentRepository(SQLAlchemyRepository):
    """Repository for performing CRUD operations and analytics on Comment
    data."""

    model = Comment

    async def get_comments_daily_breakdown(
        self,
        date_from: datetime,
        date_to: datetime,
        user_id: Optional[int] = None,
    ) -> list[CommentAnalyticSchema]:
        """Retrieve daily comment analytics within a date range, optionally
        filtered by user.

        Args:
            date_from (datetime): Start date for analytics.
            date_to (datetime): End date for analytics.
            user_id (Optional[int]): Filter comments to a specific user's posts if provided.

        Returns:
            List[CommentAnalyticSchema]: List of analytics per day with counts
            of created and blocked comments.

        """

        date_col = func.date(self.model.created_at).label("date")
        created_count = func.sum(case((~self.model.is_blocked, 1), else_=0)).label(
            "created_count",
        )
        blocked_count = func.sum(case((self.model.is_blocked, 1), else_=0)).label(
            "blocked_count",
        )

        stmt = (
            select(date_col, created_count, blocked_count)
            .join(Post, self.model.post_id == Post.id)
            .where(
                self.model.created_at >= date_from,
                self.model.created_at <= date_to,
            )
        )

        if user_id is not None:
            stmt = stmt.where(Post.user_id == user_id)

        stmt = stmt.group_by(
            func.date(
                self.model.created_at,
            ),
        ).order_by(
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
