import asyncio

from app.schemas.comments import (
    CreateCommentByPostSchema,
    ReadCommentSchema,
)
from app.schemas.posts import ReadPostSchema
from app.schemas.users import ReadUserSchema
from app.services.moderation import (
    AbstractModerationService,
    AIModerationService,
)
from app.utils.prompts.auto_reply_comment_system_prompt import REPLY_SYSTEM_PROMPT
from app.utils.unit_of_work import AbstractUnitOfWork


async def auto_reply_comment(
    uow: AbstractUnitOfWork,
    user: ReadUserSchema,
    comment: ReadCommentSchema,
    post: ReadPostSchema,
):
    await asyncio.sleep(user.auto_reply_delay)

    service: AbstractModerationService = AIModerationService()

    full_content = f"""
        Post title: {post.title}
        Post content: {post.content}
        Aim comment: {comment.content}
    """

    response = await service.prompt(
        content=full_content,
        system_content=REPLY_SYSTEM_PROMPT,
    )

    async with uow:
        await uow.comments.create(
            CreateCommentByPostSchema(
                content=response,
                post_id=comment.post_id,
                user_id=user.id,
                parent_comment_id=comment.id,
            ),
        )
