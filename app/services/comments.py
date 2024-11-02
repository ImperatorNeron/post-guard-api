from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.comments import (
    BaseCommentSchema,
    ReadCommentSchema,
    UpdateCommentSchema,
)
from app.utils.unit_of_work import AbstractUnitOfWork


class AbstractCommentService(ABC):

    @abstractmethod
    async def get_active_comments_by_post_id(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]: ...

    @abstractmethod
    async def create_comment(
        self,
        uow: AbstractUnitOfWork,
        comment_in: BaseModel,
    ) -> ReadCommentSchema: ...

    @abstractmethod
    async def get_user_comments(
        self,
        uow: AbstractUnitOfWork,
        user_id: int,
    ) -> list[ReadCommentSchema]: ...

    @abstractmethod
    async def get_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
    ) -> ReadCommentSchema: ...

    @abstractmethod
    async def update_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
        comment_in: UpdateCommentSchema,
    ) -> ReadCommentSchema: ...

    @abstractmethod
    async def delete_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
    ) -> None: ...


class CommentService(AbstractCommentService):

    async def get_active_comments_by_post_id(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]:
        return await uow.comments.fetch_by_attributes(
            post_id=post_id,
            is_blocked=False,
        )

    async def get_user_comments(
        self,
        uow: AbstractUnitOfWork,
        user_id: int,
    ) -> list[ReadCommentSchema]:
        return await uow.comments.fetch_by_attributes(
            user_id=user_id,
        )

    async def create_comment(
        self,
        uow: AbstractUnitOfWork,
        comment_in: BaseCommentSchema,
    ) -> ReadCommentSchema:
        return await uow.comments.create(item_in=comment_in)

    async def get_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
    ) -> ReadCommentSchema:
        return await uow.comments.fetch_by_id(item_id=comment_id)

    async def update_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
        comment_in: UpdateCommentSchema,
    ) -> ReadCommentSchema:
        return await uow.comments.update_by_id(
            item_id=comment_id,
            item_in=comment_in,
        )

    async def delete_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
    ) -> None:
        await uow.comments.remove_by_id(item_id=comment_id)
