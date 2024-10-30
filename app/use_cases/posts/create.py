from dataclasses import dataclass

from jwt import InvalidTokenError

from app.schemas.posts import (
    CreatePostSchema,
    CreatePostWithUserSchema,
)
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class CreatePostUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_in: CreatePostSchema,
        token: str,
    ):
        try:
            payload = await self.token_service.decode_jwt(token=token)
        except InvalidTokenError as e:
            # TODO: Custom exception
            raise ValueError(f"Invalid token error: {e}")

        pk = payload.get("sub")
        async with uow:
            post = CreatePostWithUserSchema(
                **post_in.model_dump(),
                user_id=pk,
            )
            return await self.post_service.create_post(post_in=post, uow=uow)
