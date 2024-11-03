from app.exceptions.posts import (
    PostBlockedError,
    PostNotFoundError,
)
from app.schemas.posts import UpdatePostSchema
from app.use_cases.posts.common import BasePostUseCase
from app.utils.unit_of_work import AbstractUnitOfWork


class UpdatePostUseCase(BasePostUseCase):

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
        post_in: UpdatePostSchema,
        payload: dict,
    ):
        post = await self.post_service.get_post_by_id(
            post_id=post_id,
            uow=uow,
        )

        if post is None or post.user_id != payload.get("sub"):
            raise PostNotFoundError(post_id=post_id)

        if post.is_blocked:
            raise PostBlockedError(post_id=post_id)

        new_post = await self._get_moderated_post(
            post_in=post_in,
        )

        return await self.post_service.update_post_by_id(
            post_id=post_id,
            post_in=new_post,
            uow=uow,
        )
