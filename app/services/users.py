from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.users import (
    ReadUserSchema,
    UpdateUserSchema,
)
from app.utils.unit_of_work import AbstractUnitOfWork


class AbstractUserService(ABC):

    @abstractmethod
    async def get_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> BaseModel: ...

    @abstractmethod
    async def get_user_by_id(
        self,
        uow: AbstractUnitOfWork,
        id: int,  # noqa
    ) -> BaseModel: ...

    @abstractmethod
    async def update_user(
        self,
        uow: AbstractUnitOfWork,
        user_id: int,
        user_in: UpdateUserSchema,
    ) -> BaseModel: ...


class UserService(AbstractUserService):

    async def get_user_by_username(
        self,
        uow: AbstractUnitOfWork,
        username: str,
    ) -> ReadUserSchema:
        return await uow.users.fetch_one_by_attributes(username=username)

    async def get_user_by_id(
        self,
        uow: AbstractUnitOfWork,
        id: int,  # noqa
    ) -> ReadUserSchema:
        return await uow.users.fetch_by_id(item_id=id)

    async def update_user(
        self,
        uow: AbstractUnitOfWork,
        user_id: int,
        user_in: UpdateUserSchema,
    ) -> ReadUserSchema:
        return await uow.users.update_by_id(
            item_id=user_id,
            item_in=user_in,
        )
