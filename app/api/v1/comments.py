from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import oauth2_scheme
from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.comments import (
    CreateCommentSchema,
    ReadCommentSchema,
)
from app.use_cases.comments.comments_by_post import GetCommentsByPostUseCase
from app.use_cases.comments.create import CreateCommentUseCase
from app.use_cases.comments.current_user_comments import GetUserCommentsUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/post/{post_id}",
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


@router.post(
    "/post/{post_id}",
    response_model=ApiResponseSchema[ReadCommentSchema],
)
async def create_comment(
    post_id: int,
    comment_in: CreateCommentSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: CreateCommentUseCase = container.resolve(CreateCommentUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_id=post_id,
            comment_in=comment_in,
            token=token,
        ),
    )


@router.get(
    "/me",
    response_model=ApiResponseSchema[list[ReadCommentSchema]],
)
async def get_current_user_comments(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: GetUserCommentsUseCase = container.resolve(GetUserCommentsUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            token=token,
        ),
    )
