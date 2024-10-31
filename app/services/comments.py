from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel

from app.schemas.comments import (
    BaseCommentSchema,
    ReadCommentSchema,
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
    ) -> BaseModel: ...


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

    async def create_comment(
        self,
        uow: AbstractUnitOfWork,
        comment_in: BaseCommentSchema,
    ) -> ReadCommentSchema:
        return await uow.comments.create(item_in=comment_in)
