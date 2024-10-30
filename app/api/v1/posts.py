from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import oauth2_scheme
from app.core.containers import get_container
from app.schemas.api_response import ApiResponseSchema
from app.schemas.posts import (
    CreatePostSchema,
    ReadPostSchema,
)
from app.services.posts import AbstractPostService
from app.use_cases.posts.create import CreatePostUseCase
from app.use_cases.posts.delete import DeletePostUseCase
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/users", tags=["Posts"])


@router.get(
    "/posts",
    response_model=ApiResponseSchema[list[ReadPostSchema]],
)
async def get_posts(
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
):
    posts_service: AbstractPostService = container.resolve(AbstractPostService)
    return ApiResponseSchema(data=await posts_service.get_active_posts(uow))


@router.post(
    "/posts",
    response_model=ApiResponseSchema[ReadPostSchema],
)
async def create_post(
    container: Annotated[Container, Depends(get_container)],
    post_in: CreatePostSchema,
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: CreatePostUseCase = container.resolve(CreatePostUseCase)
    return ApiResponseSchema(
        data=await use_case.execute(uow=uow, post_in=post_in, token=token),
    )


@router.delete("/posts")
async def delete_post(
    container: Annotated[Container, Depends(get_container)],
    post_id: int,
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    use_case: DeletePostUseCase = container.resolve(DeletePostUseCase)
    return await use_case.execute(uow=uow, post_id=post_id, token=token)
