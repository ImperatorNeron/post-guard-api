from dataclasses import dataclass

from app.exceptions.comments import CommentNotFoundError
from app.schemas.comments import ReadCommentSchema
from app.services.comments import AbstractCommentService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class DeleteCommentUseCase:

    comment_service: AbstractCommentService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        comment_id: int,
        token: str,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            comment: ReadCommentSchema = await self.comment_service.get_comment_by_id(
                comment_id=comment_id,
                uow=uow,
            )

            if comment is None or comment.user_id != pk:
                raise CommentNotFoundError(comment_id=comment_id)

            await self.comment_service.delete_comment_by_id(
                comment_id=comment_id,
                uow=uow,
            )
