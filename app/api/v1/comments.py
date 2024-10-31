from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.comments import ReadCommentSchema
from app.use_cases.comments.comments_by_post import GetCommentsByPostUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/{post_id}",
    response_model=ApiResponseSchema[list[ReadCommentSchema]],
)
async def get_comments_by_post_id(
    post_id: int,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    use_case: GetCommentsByPostUseCase = container.resolve(GetCommentsByPostUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_id=post_id,
        ),
    )
