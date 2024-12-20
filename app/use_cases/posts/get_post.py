from dataclasses import dataclass

from app.exceptions.posts import (
    PostBlockedError,
    PostNotFoundError,
)
from app.services.posts import AbstractPostService
from app.use_cases.posts.common import BasePostUseCase
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetPostUseCase(BasePostUseCase):

    post_service: AbstractPostService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
        payload: dict,
    ):
        post = await self.post_service.get_post_by_id(
            post_id=post_id,
            uow=uow,
        )
        if post is None:
            raise PostNotFoundError(post_id=post_id)

        if post.user_id != payload.get("sub") and post.is_blocked:
            raise PostBlockedError(post_id=post_id)

        return post
