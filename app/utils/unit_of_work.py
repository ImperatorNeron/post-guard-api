from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from app.db.db import database_helper
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository


class AbstractUnitOfWork(ABC):

    users: Type[UserRepository]
    posts: Type[PostRepository]
    comments: Type[CommentRepository]

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...


class UnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self):
        self.session = database_helper.session_factory()
        self.users = UserRepository(session=self.session)
        self.posts = PostRepository(session=self.session)
        self.comments = CommentRepository(session=self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
