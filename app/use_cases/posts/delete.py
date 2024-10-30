from dataclasses import dataclass

from jwt import InvalidTokenError

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
            if post.user_id != pk:
                # TODO: custome error
                raise ValueError("Wrong post")
            await self.post_service.delete_post_by_id(
                post_id=post_id,
                uow=uow,
            )
