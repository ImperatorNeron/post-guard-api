from datetime import datetime

from pydantic import BaseModel


class CommentAnalyticSchema(BaseModel):
    date: datetime
    created_count: int
    blocked_count: int
