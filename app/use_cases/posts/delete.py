from dataclasses import dataclass

from app.exceptions.posts import PostNotFoundError
from app.schemas.posts import ReadPostSchema
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class DeletePostUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_id: int,
        payload: dict,
    ):
        post: ReadPostSchema = await self.post_service.get_post_by_id(
            post_id=post_id,
            uow=uow,
        )

        if post is None or post.user_id != payload.get("sub"):
            raise PostNotFoundError(post_id=post_id)

        await self.post_service.delete_post_by_id(
            post_id=post_id,
            uow=uow,
        )
