from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
from typing import Optional

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

    @abstractmethod
    async def get_comments_daily_breakdown(
        self,
        uow: AbstractUnitOfWork,
        date_from: datetime,
        date_to: datetime,
        user_id: Optional[int] = None,
    ): ...

    @abstractmethod
    async def get_comments_by_parent_comment_id(
        self,
        uow: AbstractUnitOfWork,
        parent_comment_id: Optional[int],
    ) -> list[ReadCommentSchema]: ...


class CommentService(AbstractCommentService):

    async def get_active_comments_by_post_id(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]:
        async with uow:
            return await uow.comments.fetch_by_attributes(
                post_id=post_id,
                is_blocked=False,
            )

    async def get_user_comments(
        self,
        uow: AbstractUnitOfWork,
        user_id: int,
    ) -> list[ReadCommentSchema]:
        async with uow:
            return await uow.comments.fetch_by_attributes(
                user_id=user_id,
            )

    async def create_comment(
        self,
        uow: AbstractUnitOfWork,
        comment_in: BaseCommentSchema,
    ) -> ReadCommentSchema:
        async with uow:
            return await uow.comments.create(item_in=comment_in)

    async def get_comment_by_id(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
    ) -> ReadCommentSchema:
        async with uow:
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
        async with uow:
            await uow.comments.remove_by_id(item_id=comment_id)

    async def get_comments_daily_breakdown(
        self,
        uow: AbstractUnitOfWork,
        date_from: datetime,
        date_to: datetime,
        user_id: Optional[int] = None,
    ):
        async with uow:
            return await uow.comments.get_comments_daily_breakdown(
                date_from=date_from,
                date_to=date_to,
                user_id=user_id,
            )

    async def get_comments_by_parent_comment_id(
        self,
        uow: AbstractUnitOfWork,
        parent_comment_id: Optional[int],
    ) -> list[ReadCommentSchema]:
        async with uow:
            return await uow.comments.fetch_by_attributes(
                parent_comment_id=parent_comment_id,
                is_blocked=False,
            )
