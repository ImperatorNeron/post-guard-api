from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from app.schemas.comments import (
    CreateCommentByPostSchema,
    ModerateCommentSchema,
    UpdateCommentSchema,
    UpdateModerateCommentSchema,
)
from app.services.comments import AbstractCommentService
from app.services.moderation import AbstractModerationService
from app.services.posts import AbstractPostService


@dataclass
class BaseCommentUseCase:

    post_service: AbstractPostService
    comment_service: AbstractCommentService
    moderation_service: AbstractModerationService

    async def _get_moderated_comment(
        self,
        comment_in: BaseModel,
        post_id: Optional[int] = None,
        user_id: Optional[int] = None,
    ) -> BaseModel:
        moderation_result = await self.moderation_service.check_content(
            comment_in.content,
        )

        if user_id is not None:
            if moderation_result.get("is_blocked"):
                return ModerateCommentSchema(
                    **comment_in.model_dump(),
                    **moderation_result,
                    user_id=user_id,
                    post_id=post_id,
                )
            return CreateCommentByPostSchema(
                **comment_in.model_dump(),
                user_id=user_id,
                post_id=post_id,
            )

        if moderation_result.get("is_blocked"):
            return UpdateModerateCommentSchema(
                **comment_in.model_dump(exclude_unset=True),
                **moderation_result,
            )

        return UpdateCommentSchema(
            **comment_in.model_dump(exclude_unset=True),
        )
