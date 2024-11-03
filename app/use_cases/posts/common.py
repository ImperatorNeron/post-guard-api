from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from app.schemas.posts import (
    CreatePostWithUserSchema,
    ModeratePostSchema,
    UpdateModeratePostSchema,
    UpdatePostSchema,
)
from app.services.moderation import AbstractModerationService
from app.services.posts import AbstractPostService


@dataclass
class BasePostUseCase:

    post_service: AbstractPostService
    moderation_service: AbstractModerationService

    async def _get_moderated_post(
        self,
        post_in: BaseModel,
        user_id: Optional[int] = None,
    ) -> BaseModel:
        moderation_result = await self.moderation_service.check_content(
            post_in.title,
            post_in.content,
        )

        if user_id is not None:
            if moderation_result.get("is_blocked"):
                return ModeratePostSchema(
                    **post_in.model_dump(exclude_unset=True),
                    **moderation_result,
                    user_id=user_id,
                )
            return CreatePostWithUserSchema(
                **post_in.model_dump(exclude_unset=True),
                user_id=user_id,
            )

        if moderation_result.get("is_blocked"):
            return UpdateModeratePostSchema(
                **post_in.model_dump(exclude_unset=True),
                **moderation_result,
            )

        return UpdatePostSchema(
            **post_in.model_dump(exclude_unset=True),
        )
