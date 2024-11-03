from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import get_current_token_payload
from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.posts import (
    CreatePostSchema,
    ReadPostSchema,
    UpdatePostSchema,
)
from app.services.posts import AbstractPostService
from app.use_cases.posts.create import CreatePostUseCase
from app.use_cases.posts.delete import DeletePostUseCase
from app.use_cases.posts.get_post import GetPostUseCase
from app.use_cases.posts.update import UpdatePostUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get(
    "",
    response_model=ApiResponseSchema[list[ReadPostSchema]],
)
async def get_posts(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    service: AbstractPostService = container.resolve(AbstractPostService)
    return ApiResponseSchema(data=await service.get_active_posts(uow=uow))


@router.get(
    "/my",
    response_model=ApiResponseSchema[list[ReadPostSchema]],
)
async def get_current_user_posts(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    service: AbstractPostService = container.resolve(AbstractPostService)
    return ApiResponseSchema(
        data=await service.get_posts_by_user_id(
            user_id=payload.get("sub"),
            uow=uow,
        ),
    )


@router.get(
    "/{post_id}",
    response_model=ApiResponseSchema[ReadPostSchema],
)
async def get_post(
    post_id: int,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: GetPostUseCase = container.resolve(GetPostUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_id=post_id,
            payload=payload,
        ),
    )


@router.post(
    "",
    response_model=ApiResponseSchema[ReadPostSchema],
)
async def create_post(
    container: Annotated[Container, Depends(get_container)],
    post_in: CreatePostSchema,
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: CreatePostUseCase = container.resolve(CreatePostUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_in=post_in,
            payload=payload,
        ),
    )


@router.patch(
    "/{post_id}",
    response_model=ApiResponseSchema[ReadPostSchema],
)
async def update_post(
    container: Annotated[Container, Depends(get_container)],
    post_id: int,
    post_in: UpdatePostSchema,
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: UpdatePostUseCase = container.resolve(UpdatePostUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(
            uow=uow,
            post_id=post_id,
            post_in=post_in,
            payload=payload,
        ),
    )


@router.delete("/{post_id}")
async def delete_post(
    container: Annotated[Container, Depends(get_container)],
    post_id: int,
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    use_case: DeletePostUseCase = container.resolve(DeletePostUseCase)
    return await use_case.execute(
        uow=uow,
        post_id=post_id,
        payload=payload,
    )
