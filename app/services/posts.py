from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.posts import (
    CreatePostWithUserSchema,
    ReadPostSchema,
)
from app.utils.unit_of_work import AbstractUnitOfWork


class AbstractPostService(ABC):

    @abstractmethod
    async def get_active_posts(
        self,
        uow: AbstractUnitOfWork,
    ) -> list[BaseModel]: ...

    @abstractmethod
    async def create_post(
        self,
        uow: AbstractUnitOfWork,
        post_in: BaseModel,
    ) -> BaseModel: ...


class PostService(AbstractPostService):

    async def get_active_posts(
        self,
        uow: AbstractUnitOfWork,
    ) -> list[ReadPostSchema]:
        async with uow:
            return await uow.posts.fetch_by_attributes(is_blocked=False)

    async def create_post(
        self,
        uow: AbstractUnitOfWork,
        post_in: CreatePostWithUserSchema,
    ) -> ReadPostSchema:
        async with uow:
            return await uow.posts.create(item_in=post_in)
