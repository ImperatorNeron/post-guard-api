from app.models.posts import Post
from app.utils.sql_repository import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):
    """Repository for performing CRUD operations on Post data."""

    model = Post
