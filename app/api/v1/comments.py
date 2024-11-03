from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import get_current_token_payload
from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.comments import (
    CreateCommentSchema,
    ReadCommentSchema,
    UpdateCommentSchema,
)
from app.services.comments import AbstractCommentService
from app.use_cases.comments.comments_by_post import GetCommentsByPostUseCase
from app.use_cases.comments.create import CreateCommentUseCase
from app.use_cases.comments.delete import DeleteCommentUseCase
from app.use_cases.comments.update import UpdateCommentUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get(
    "/posts/{post_id}",
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
    "/posts/{post_id}",
    response_model=ApiResponseSchema[ReadCommentSchema],
)
async def create_comment(
    post_id: int,
    background_tasks: BackgroundTasks,
    comment_in: CreateCommentSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: CreateCommentUseCase = container.resolve(CreateCommentUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_id=post_id,
            comment_in=comment_in,
            payload=payload,
            background_tasks=background_tasks,
        ),
    )


@router.get(
    "/{parent_comment_id}/replies/",
    response_model=ApiResponseSchema[list[ReadCommentSchema]],
)
async def get_comments_by_parent_comment_id(
    parent_comment_id: int,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    service: AbstractCommentService = container.resolve(AbstractCommentService)
    return ApiResponseSchema(
        data=await service.get_comments_by_parent_comment_id(
            uow=uow,
            parent_comment_id=parent_comment_id,
        ),
    )


@router.get(
    "/my",
    response_model=ApiResponseSchema[list[ReadCommentSchema]],
)
async def get_current_user_comments(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    service: AbstractCommentService = container.resolve(AbstractCommentService)
    return ApiResponseSchema(
        data=await service.get_user_comments(
            uow=uow,
            user_id=payload.get("sub"),
        ),
    )


@router.patch(
    "/{comment_id}",
    response_model=ApiResponseSchema[ReadCommentSchema],
)
async def update_current_user_comments(
    comment_id: int,
    comment_in: UpdateCommentSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: UpdateCommentUseCase = container.resolve(UpdateCommentUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            payload=payload,
            comment_in=comment_in,
            comment_id=comment_id,
        ),
    )


@router.delete("/{comment_id}")
async def delete_current_user_comments(
    comment_id: int,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: DeleteCommentUseCase = container.resolve(DeleteCommentUseCase)
    await use_case.execute(
        uow=uow,
        payload=payload,
        comment_id=comment_id,
    )
