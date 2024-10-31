from dataclasses import dataclass

from app.schemas.posts import (
    CreatePostSchema,
    CreatePostWithUserSchema,
    ModeratePostSchema,
)
from app.services.moderation import AbstractModerationService
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class CreatePostUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService
    moderation_service: AbstractModerationService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_in: CreatePostSchema,
        token: str,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:

            moderation_result = await self.moderation_service.check_content(
                post_in.title,
                post_in.content,
            )

            if moderation_result.get("is_blocked"):
                post = ModeratePostSchema(
                    **post_in.model_dump(),
                    **moderation_result,
                    user_id=pk,
                )
            else:
                post = CreatePostWithUserSchema(
                    **post_in.model_dump(),
                    user_id=pk,
                )
            return await self.post_service.create_post(post_in=post, uow=uow)
