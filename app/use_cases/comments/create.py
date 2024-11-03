from dataclasses import dataclass

from app.exceptions.comments import CommentBlockedPostError
from app.exceptions.posts import PostNotFoundError
from app.schemas.comments import (
    CreateCommentByPostSchema,
    CreateCommentSchema,
    ModerateCommentSchema,
)
from app.schemas.posts import ReadPostSchema
from app.services.comments import AbstractCommentService
from app.services.moderation import AbstractModerationService
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class CreateCommentUseCase:

    token_service: AbstractJWTTokenService
    post_service: AbstractPostService
    comment_service: AbstractCommentService
    moderation_service: AbstractModerationService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        comment_in: CreateCommentSchema,
        post_id: int,
        token: str,
        parent_comment_id: int = None,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            post: ReadPostSchema = await self.post_service.get_post_by_id(
                uow=uow,
                post_id=post_id,
            )

            if post is None:
                raise PostNotFoundError(post_id=post_id)

            if post.is_blocked:
                raise CommentBlockedPostError(post_id=post_id)
            moderation_result = await self.moderation_service.check_content(
                comment_in.content,
            )
            if moderation_result.get("is_blocked"):
                comment = ModerateCommentSchema(
                    **comment_in.model_dump(),
                    **moderation_result,
                    user_id=pk,
                    post_id=post_id,
                    parent_comment_id=parent_comment_id,
                )
            else:
                comment = CreateCommentByPostSchema(
                    **comment_in.model_dump(),
                    user_id=pk,
                    post_id=post_id,
                    parent_comment_id=parent_comment_id,
                )
            return await self.comment_service.create_comment(
                uow=uow,
                comment_in=comment,
            )
