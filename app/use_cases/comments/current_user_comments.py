from dataclasses import dataclass

from app.schemas.comments import ReadCommentSchema
from app.services.comments import AbstractCommentService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetUserCommentsUseCase:

    comment_service: AbstractCommentService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        uow: AbstractUnitOfWork,
        token: str,
    ) -> list[ReadCommentSchema]:
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        async with uow:
            return await self.comment_service.get_user_comments(
                user_id=pk,
                uow=uow,
            )
