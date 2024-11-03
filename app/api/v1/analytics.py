from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import get_current_token_payload
from app.core.containers import get_container
from app.schemas.analytics import CommentAnalyticSchema
from app.schemas.api_response import ApiResponseSchema
from app.services.comments import AbstractCommentService
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    path="/comments-daily-breakdown",
    response_model=ApiResponseSchema[list[CommentAnalyticSchema]],
)
async def get_comments_daily_breakdown(
    date_from: datetime,
    date_to: datetime,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    service: AbstractCommentService = container.resolve(AbstractCommentService)
    return ApiResponseSchema(
        data=await service.get_comments_daily_breakdown(
            uow=uow,
            date_from=date_from,
            date_to=date_to,
        ),
    )


@router.get(
    path="/current-user-comments-daily-breakdown",
    response_model=ApiResponseSchema[list[CommentAnalyticSchema]],
)
async def get_current_user_comments_daily_breakdown(
    date_from: datetime,
    date_to: datetime,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    service: AbstractCommentService = container.resolve(AbstractCommentService)
    return ApiResponseSchema(
        data=await service.get_comments_daily_breakdown(
            uow=uow,
            date_from=date_from,
            date_to=date_to,
            user_id=payload.get("sub"),
        ),
    )
