from app.exceptions.comments import CommentBlockedPostError
from app.exceptions.posts import PostNotFoundError
from app.schemas.comments import CreateCommentSchema
from app.schemas.posts import ReadPostSchema
from app.use_cases.comments.common import BaseCommentUseCase
from app.utils.unit_of_work import AbstractUnitOfWork


class CreateCommentUseCase(BaseCommentUseCase):

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        comment_in: CreateCommentSchema,
        post_id: int,
        payload: dict,
    ):
        post: ReadPostSchema = await self.post_service.get_post_by_id(
            uow=uow,
            post_id=post_id,
        )

        if post is None:
            raise PostNotFoundError(post_id=post_id)

        if post.is_blocked:
            raise CommentBlockedPostError(post_id=post_id)

        new_comment = await self._get_moderated_comment(
            comment_in=comment_in,
            post_id=post_id,
            user_id=payload.get("sub"),
        )

        return await self.comment_service.create_comment(
            uow=uow,
            comment_in=new_comment,
        )
