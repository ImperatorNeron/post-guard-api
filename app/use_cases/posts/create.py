from app.schemas.posts import CreatePostSchema
from app.use_cases.posts.common import BasePostUseCase
from app.utils.unit_of_work import AbstractUnitOfWork


class CreatePostUseCase(BasePostUseCase):

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        post_in: CreatePostSchema,
        payload: dict,
    ):
        post = await self._get_moderated_post(
            post_in=post_in,
            user_id=payload.get("sub"),
        )
        return await self.post_service.create_post(post_in=post, uow=uow)
