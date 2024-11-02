from dataclasses import dataclass

from app.exceptions.posts import (
    PostBlockedError,
    PostNotFoundError,
)
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetPostUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
        token: str,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            post = await self.post_service.get_post_by_id(
                post_id=post_id,
                uow=uow,
            )
            if post is None:
                raise PostNotFoundError(post_id=post_id)
            if post.user_id != pk and post.is_blocked:
                # change
                raise PostBlockedError(post_id=post_id)
            return await self.post_service.get_post_by_id(
                post_id=post_id,
                uow=uow,
            )
