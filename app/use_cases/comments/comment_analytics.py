from dataclasses import dataclass
from datetime import datetime

from app.schemas.tokens import TokenInfoSchema
from app.services.comments import AbstractCommentService
from app.services.tokens import AbstractJWTTokenService
from app.utils.unit_of_work import AbstractUnitOfWork


@dataclass
class GetCurrentUserCommentsAnalyticsUseCase:

    comment_service: AbstractCommentService
    token_service: AbstractJWTTokenService

    async def execute(
        self,
        date_from: datetime,
        date_to: datetime,
        token: TokenInfoSchema,
        uow: AbstractUnitOfWork,
    ):
        payload = await self.token_service.decode_jwt(token=token)
        pk = payload.get("sub")

        return await self.comment_service.get_comments_daily_breakdown(
            uow=uow,
            date_from=date_from,
            date_to=date_to,
            user_id=pk,
        )
