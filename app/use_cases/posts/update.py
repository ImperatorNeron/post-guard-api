from dataclasses import dataclass

from app.exceptions.posts import (
    PostBlockedError,
    PostNotFoundError,
)
from app.schemas.posts import (
    ReadPostSchema,
    UpdatePostSchema,
)
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class UpdatePostUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
        post_in: UpdatePostSchema,
        token: str,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            post: ReadPostSchema = await self.post_service.get_post_by_id(
                post_id=post_id,
                uow=uow,
            )

            if post is None or post.user_id != pk:
                raise PostNotFoundError(post_id=post_id)

            if post.is_blocked:
                raise PostBlockedError(post_id=post_id)

            return await self.post_service.update_post_by_id(
                post_id=post_id,
                post_in=post_in,
                uow=uow,
            )
