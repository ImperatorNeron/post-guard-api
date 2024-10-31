from dataclasses import dataclass

from app.exceptions.posts import PostNotFoundError
from app.schemas.comments import ReadCommentSchema
from app.services.comments import AbstractCommentService
from app.services.posts import AbstractPostService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetCommentsByPostUseCase:

    post_service: AbstractPostService
    comment_service: AbstractCommentService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
    ) -> list[ReadCommentSchema]:

        async with uow:
            post = await self.post_service.get_post_by_id(
                post_id=post_id,
                uow=uow,
            )

            if post is None:
                raise PostNotFoundError(post_id)

            return await self.comment_service.get_active_comments_by_post_id(
                uow=uow,
                post_id=post_id,
            )
