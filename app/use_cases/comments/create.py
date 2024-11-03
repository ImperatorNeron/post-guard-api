from fastapi import BackgroundTasks

from app.background_tasks.auto_reply_comment_task import auto_reply_comment
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
        background_tasks: BackgroundTasks,
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

        created_comment = await self.comment_service.create_comment(
            uow=uow,
            comment_in=new_comment,
        )

        user = await self.user_service.get_user_by_id(uow=uow, id=post.user_id)

        if user.is_auto_reply_enabled and not created_comment.is_blocked:
            background_tasks.add_task(
                auto_reply_comment,
                uow,
                user,
                created_comment,
                post,
            )

        return created_comment
