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
    async def get_post_by_id(
        self,
        post_id: int,
        uow: AbstractUnitOfWork,
    ) -> BaseModel: ...

    @abstractmethod
    async def get_posts_by_user_id(
        self,
        user_id: int,
        uow: AbstractUnitOfWork,
    ) -> list[BaseModel]: ...

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

    @abstractmethod
    async def delete_post_by_id(
        self,
        post_id: int,
        uow: AbstractUnitOfWork,
    ) -> None: ...


class PostService(AbstractPostService):

    async def get_post_by_id(
        self,
        post_id: int,
        uow: AbstractUnitOfWork,
    ) -> ReadPostSchema:
        return await uow.posts.fetch_by_id(post_id)

    async def get_posts_by_user_id(
        self,
        user_id: int,
        uow: AbstractUnitOfWork,
    ) -> list[ReadPostSchema]:
        return await uow.posts.fetch_by_attributes(user_id=user_id)

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
        return await uow.posts.create(item_in=post_in)

    async def delete_post_by_id(
        self,
        post_id: int,
        uow: AbstractUnitOfWork,
    ):
        async with uow:
            return await uow.posts.remove_by_id(item_id=post_id)
