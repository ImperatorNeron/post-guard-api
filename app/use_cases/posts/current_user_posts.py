from dataclasses import dataclass

from app.schemas.posts import ReadPostSchema
from app.services.posts import AbstractPostService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetUserPostsUseCase:

    post_service: AbstractPostService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        token: str,
    ) -> list[ReadPostSchema]:
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            return await self.post_service.get_posts_by_user_id(
                user_id=pk,
                uow=uow,
            )
