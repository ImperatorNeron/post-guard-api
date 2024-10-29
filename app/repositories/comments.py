from app.models.comments import Comment
from app.utils.sql_repository import SQLAlchemyRepository


class CommentRepository(SQLAlchemyRepository):

    model = Comment
