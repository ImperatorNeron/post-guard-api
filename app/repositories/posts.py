from app.models.posts import Post
from app.utils.sql_repository import SQLAlchemyRepository


class PostRepository(SQLAlchemyRepository):

    model = Post
