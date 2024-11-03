from dataclasses import dataclass

from app.exceptions.comments import CommentNotFoundError
from app.services.comments import AbstractCommentService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class DeleteCommentUseCase:

    comment_service: AbstractCommentService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
        payload: dict,
    ):
        comment = await self.comment_service.get_comment_by_id(
            comment_id=comment_id,
            uow=uow,
        )

        if comment is None or comment.user_id != payload.get("sub"):
            raise CommentNotFoundError(comment_id=comment_id)

        await self.comment_service.delete_comment_by_id(
            comment_id=comment_id,
            uow=uow,
        )
