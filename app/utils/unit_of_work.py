from abc import (
    ABC,
    abstractmethod,
)

from app.db.db import database_helper


class AbstractUnitOfWork(ABC):

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
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
