from app.models.users import User
from app.utils.sql_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):

    model = User
