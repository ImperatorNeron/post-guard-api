from dataclasses import dataclass

from jwt import InvalidTokenError

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
        # TODO: do this in apart file
        try:
            payload = await self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            # TODO: Custom exception
            raise ValueError(f"Invalid token error: {e}")

        pk = payload.get("sub")

        async with uow:
            post: ReadPostSchema = await self.post_service.get_post_by_id(
                post_id=post_id,
                uow=uow,
            )
            # TODO: custome error
            if post is None or post.user_id != pk:
                raise ValueError("Wrong post")
            if post.is_blocked:
                raise ValueError("This post was blocked and cannot be changed!")
            return await self.post_service.update_post_by_id(
                post_id=post_id,
                post_in=post_in,
                uow=uow,
            )
