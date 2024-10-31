from abc import (
    ABC,
    abstractmethod,
)

from app.schemas.comments import ReadCommentSchema
from app.utils.unit_of_work import AbstractUnitOfWork


class AbstractCommentService(ABC):

    @abstractmethod
    async def get_comments_by_post_id(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]: ...


class CommentService(AbstractCommentService):

    async def get_comments_by_post_id(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]:
        return await uow.comments.fetch_by_attributes(post_id=post_id)
