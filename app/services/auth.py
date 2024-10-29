from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.users import (
    CreateUserSchema,
    ReadUserSchema,
)
from app.utils.unit_of_work import AbstractUnitOfWork


class AbstractAuthService(ABC):

    @abstractmethod
    async def register(
        self,
        uow: AbstractUnitOfWork,
        user_in: CreateUserSchema,
    ) -> BaseModel: ...

    @abstractmethod
    async def get_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> BaseModel: ...


class AuthService(AbstractAuthService):

    async def register(
        self,
        uow: AbstractUnitOfWork,
        user_in: CreateUserSchema,
    ) -> ReadUserSchema:
        return await uow.users.create(item_in=user_in)

    async def get_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> ReadUserSchema:
        return await uow.users.fetch_one_by_attributes(username=username)
