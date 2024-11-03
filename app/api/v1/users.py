from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from punq import Container

from app.api.v1.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
)
from app.core.containers import get_container
from app.schemas.users import (
    ReadUserSchema,
    UpdateUserSchema,
)
from app.services.users import AbstractUserService
from app.utils.unit_of_work import (
    AbstractUnitOfWork,
    UnitOfWork,
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.patch(
    "/me",
    response_model=ReadUserSchema,
)
async def update_user_profile(
    user_in: UpdateUserSchema,
    container: Annotated[Container, Depends(get_container)],
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork)],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    service: AbstractUserService = container.resolve(AbstractUserService)
    return await service.update_user(
        user_id=payload.get("sub"),
        user_in=user_in,
        uow=uow,
    )


@router.get(
    "/me",
    response_model=ReadUserSchema,
)
async def get_authenticated_user_profile(
    user: Annotated[ReadUserSchema, Depends(get_current_active_auth_user)],
):
    return user
