from app.exceptions.comments import (
    CommentBlockedError,
    CommentNotFoundError,
)
from app.schemas.comments import (
    ReadCommentSchema,
    UpdateCommentSchema,
)
from app.use_cases.comments.common import BaseCommentUseCase
from app.utils.unit_of_work import AbstractUnitOfWork


class UpdateCommentUseCase(BaseCommentUseCase):

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
        comment_in: UpdateCommentSchema,
        payload: dict,
    ):
        comment: ReadCommentSchema = await self.comment_service.get_comment_by_id(
            comment_id=comment_id,
            uow=uow,
        )

        if comment is None or comment.user_id != payload.get("sub"):
            raise CommentNotFoundError(comment_id=comment_id)

        if comment.is_blocked:
            raise CommentBlockedError(comment_id=comment_id)

        new_comment = await self._get_moderated_comment(
            comment_in=comment_in,
        )

        return await self.comment_service.update_comment_by_id(
            comment_id=comment_id,
            comment_in=new_comment,
            uow=uow,
        )
