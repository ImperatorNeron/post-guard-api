from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from app.db.db import (
    database_helper,
    test_database_helper,
)
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository


class AbstractUnitOfWork(ABC):
    """Abstract base class defining a unit of work pattern for managing
    repositories and database transactions."""

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


class BaseUnitOfWork(AbstractUnitOfWork):
    async def __aenter__(self):
        self.session = await self._get_session()
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

    @abstractmethod
    async def _get_session(self): ...


class UnitOfWork(BaseUnitOfWork):
    """Implementation of the UnitOfWork pattern."""

    async def _get_session(self):
        return database_helper.session_factory()


class TestUnitOfWork(BaseUnitOfWork):
    """Implementation of the UnitOfWork pattern for tests."""

    async def _get_session(self):
        return test_database_helper.session_factory()
